from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.hybrid import hybrid_property
from database import Base

class Panel(Base):
    __tablename__ = "panels"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    model = Column(String)  # e.g., "Hager Volta"
    manufacturer = Column(String, default="Hager")
    rows = Column(Integer, default=2)  # Number of rows in the panel
    slots_per_row = Column(Integer)  # Number of slots per row
    voltage = Column(Float)  # e.g., 230V, 400V
    current_rating = Column(Float)  # e.g., 63A, 100A
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    @hybrid_property
    def total_slots(self):
        return self.rows * self.slots_per_row
    
    # Relationships
    slots = relationship("PanelSlot", back_populates="panel")
    wires = relationship("Wire", back_populates="panel")

class DeviceType(Base):
    __tablename__ = "device_types"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)  # e.g., "Circuit Breaker", "RCD", "Smart Meter"
    category = Column(String)  # e.g., "Protection", "Measurement", "Control"
    manufacturer = Column(String)
    model = Column(String)
    slots_required = Column(Integer, default=1)  # How many slots this device occupies
    max_current = Column(Float, nullable=True)
    voltage_range = Column(String, nullable=True)  # e.g., "230-400V"
    description = Column(Text, nullable=True)
    
    # Relationships
    panel_slots = relationship("PanelSlot", back_populates="device_type")

class PanelSlot(Base):
    __tablename__ = "panel_slots"
    
    id = Column(Integer, primary_key=True, index=True)
    panel_id = Column(Integer, ForeignKey("panels.id"))
    slot_number = Column(Integer)  # Position in the panel (1-based)
    row = Column(Integer)  # Row number (1-based)
    column = Column(Integer)  # Column number within the row (1-based)
    device_type_id = Column(Integer, ForeignKey("device_types.id"), nullable=True)
    device_label = Column(String, nullable=True)  # Custom label for this instance
    current_setting = Column(Float, nullable=True)  # e.g., breaker trip current
    is_occupied = Column(Boolean, default=False)
    spans_slots = Column(Integer, default=1)  # For devices that span multiple slots
    
    # Relationships
    panel = relationship("Panel", back_populates="slots")
    device_type = relationship("DeviceType", back_populates="panel_slots")
    input_wires = relationship("Wire", foreign_keys="[Wire.destination_slot_id]", back_populates="destination_slot")
    output_wires = relationship("Wire", foreign_keys="[Wire.source_slot_id]", back_populates="source_slot")

class Wire(Base):
    __tablename__ = "wires"
    
    id = Column(Integer, primary_key=True, index=True)
    panel_id = Column(Integer, ForeignKey("panels.id"))
    label = Column(String)  # e.g., "L1", "N", "PE", "Kitchen Lights"
    wire_type = Column(String)  # e.g., "Live", "Neutral", "Earth", "Data"
    cross_section = Column(Float)  # Wire cross-section in mm²
    color = Column(String, nullable=True)  # Wire color
    source_slot_id = Column(Integer, ForeignKey("panel_slots.id"), nullable=True)
    destination_slot_id = Column(Integer, ForeignKey("panel_slots.id"), nullable=True)
    external_source = Column(String, nullable=True)  # e.g., "Main Supply", "External Circuit"
    external_destination = Column(String, nullable=True)  # e.g., "Kitchen Outlet", "Living Room Lights"
    length = Column(Float, nullable=True)  # Wire length in meters
    
    # Relationships
    panel = relationship("Panel", back_populates="wires")
    source_slot = relationship("PanelSlot", foreign_keys=[source_slot_id], back_populates="output_wires")
    destination_slot = relationship("PanelSlot", foreign_keys=[destination_slot_id], back_populates="input_wires")
