from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.hybrid import hybrid_property
from database import Base

class PanelTemplate(Base):
    __tablename__ = "panel_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)  # e.g., "Hager Volta VU24NW"
    model = Column(String)  # e.g., "VU24NW"
    manufacturer = Column(String, default="Hager")
    series = Column(String, nullable=True)  # e.g., "Volta"
    rows = Column(Integer, default=2)  # Number of rows in the panel
    slots_per_row = Column(Integer)  # Number of slots per row
    voltage = Column(Float)  # e.g., 230V, 400V
    max_current = Column(Float)  # e.g., 63A, 100A
    enclosure_type = Column(String, nullable=True)  # e.g., "Surface", "Flush"
    protection_rating = Column(String, nullable=True)  # e.g., "IP40", "IP65"
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)  # For soft delete/deactivation
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    @hybrid_property
    def total_slots(self):
        return self.rows * self.slots_per_row
    
    # Relationships
    panels = relationship("Panel", back_populates="template")

class DeviceTemplate(Base):
    __tablename__ = "device_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)  # e.g., "MCB 16A C-Curve"
    model = Column(String)  # e.g., "MBN116"
    manufacturer = Column(String, default="Hager")
    series = Column(String, nullable=True)  # e.g., "MBN"
    device_type = Column(String)  # e.g., "MCB", "RCD", "RCBO", "Smart Meter"
    category = Column(String)  # e.g., "Protection", "Measurement", "Control"
    slots_required = Column(Integer, default=1)  # How many slots this device occupies
    rated_current = Column(Float, nullable=True)  # Nominal current rating
    max_current = Column(Float, nullable=True)  # Maximum current rating
    voltage_range = Column(String, nullable=True)  # e.g., "230-400V"
    breaking_capacity = Column(Float, nullable=True)  # kA for circuit breakers
    sensitivity = Column(Float, nullable=True)  # mA for RCDs
    curve_type = Column(String, nullable=True)  # B, C, D for MCBs
    pole_count = Column(Integer, nullable=True)  # 1P, 2P, 3P, 4P
    width_in_modules = Column(Float, default=1.0)  # Physical width (1 module = 18mm)
    mounting_type = Column(String, nullable=True)  # "DIN Rail", "Panel Mount"
    features = Column(Text, nullable=True)  # JSON string for additional features
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)  # For soft delete/deactivation
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    device_instances = relationship("PanelSlot", back_populates="device_template")

class Panel(Base):
    __tablename__ = "panels"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)  # Instance-specific name
    template_id = Column(Integer, ForeignKey("panel_templates.id"))
    location = Column(String, nullable=True)  # Installation location
    installation_date = Column(DateTime(timezone=True), nullable=True)
    description = Column(Text, nullable=True)  # Instance-specific description
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    template = relationship("PanelTemplate", back_populates="panels")
    slots = relationship("PanelSlot", back_populates="panel")
    wires = relationship("Wire", back_populates="panel")

class PanelSlot(Base):
    __tablename__ = "panel_slots"
    
    id = Column(Integer, primary_key=True, index=True)
    panel_id = Column(Integer, ForeignKey("panels.id"))
    slot_number = Column(Integer)  # Position in the panel (1-based)
    row = Column(Integer)  # Row number (1-based)
    column = Column(Integer)  # Column number within the row (1-based)
    device_template_id = Column(Integer, ForeignKey("device_templates.id"), nullable=True)
    device_label = Column(String, nullable=True)  # Custom label for this instance
    current_setting = Column(Float, nullable=True)  # e.g., breaker trip current
    custom_properties = Column(Text, nullable=True)  # JSON string for instance-specific properties
    is_occupied = Column(Boolean, default=False)
    spans_slots = Column(Integer, default=1)  # For devices that span multiple slots
    installed_date = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    panel = relationship("Panel", back_populates="slots")
    device_template = relationship("DeviceTemplate", back_populates="device_instances")
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
