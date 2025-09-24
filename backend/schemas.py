from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Panel Schemas
class PanelBase(BaseModel):
    name: str
    model: str
    manufacturer: str = "Hager"
    total_slots: int
    voltage: float
    current_rating: float
    description: Optional[str] = None

class PanelCreate(PanelBase):
    pass

class PanelUpdate(BaseModel):
    name: Optional[str] = None
    model: Optional[str] = None
    manufacturer: Optional[str] = None
    total_slots: Optional[int] = None
    voltage: Optional[float] = None
    current_rating: Optional[float] = None
    description: Optional[str] = None

class Panel(PanelBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Device Type Schemas
class DeviceTypeBase(BaseModel):
    name: str
    category: str
    manufacturer: str
    model: str
    slots_required: int = 1
    max_current: Optional[float] = None
    voltage_range: Optional[str] = None
    description: Optional[str] = None

class DeviceTypeCreate(DeviceTypeBase):
    pass

class DeviceType(DeviceTypeBase):
    id: int
    
    class Config:
        from_attributes = True

# Panel Slot Schemas
class PanelSlotBase(BaseModel):
    slot_number: int
    device_label: Optional[str] = None
    current_setting: Optional[float] = None
    spans_slots: int = 1

class PanelSlotCreate(PanelSlotBase):
    panel_id: int
    device_type_id: Optional[int] = None

class PanelSlotUpdate(BaseModel):
    device_type_id: Optional[int] = None
    device_label: Optional[str] = None
    current_setting: Optional[float] = None
    spans_slots: Optional[int] = None

class PanelSlot(PanelSlotBase):
    id: int
    panel_id: int
    device_type_id: Optional[int] = None
    is_occupied: bool
    device_type: Optional[DeviceType] = None
    
    class Config:
        from_attributes = True

# Wire Schemas
class WireBase(BaseModel):
    label: str
    wire_type: str
    cross_section: float
    color: Optional[str] = None
    external_source: Optional[str] = None
    external_destination: Optional[str] = None
    length: Optional[float] = None

class WireCreate(WireBase):
    panel_id: int
    source_slot_id: Optional[int] = None
    destination_slot_id: Optional[int] = None

class WireUpdate(BaseModel):
    label: Optional[str] = None
    wire_type: Optional[str] = None
    cross_section: Optional[float] = None
    color: Optional[str] = None
    source_slot_id: Optional[int] = None
    destination_slot_id: Optional[int] = None
    external_source: Optional[str] = None
    external_destination: Optional[str] = None
    length: Optional[float] = None

class Wire(WireBase):
    id: int
    panel_id: int
    source_slot_id: Optional[int] = None
    destination_slot_id: Optional[int] = None
    
    class Config:
        from_attributes = True

# Extended schemas with relationships
class PanelWithSlots(Panel):
    slots: List[PanelSlot] = []

class PanelSlotWithWires(PanelSlot):
    input_wires: List[Wire] = []
    output_wires: List[Wire] = []
