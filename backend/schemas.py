from pydantic import BaseModel, computed_field
from typing import Optional, List
from datetime import datetime

# Panel Template Schemas
class PanelTemplateBase(BaseModel):
    name: str
    model: str
    manufacturer: str = "Hager"
    series: Optional[str] = None
    rows: int = 2
    slots_per_row: int
    voltage: float
    max_current: float
    enclosure_type: Optional[str] = None
    protection_rating: Optional[str] = None
    description: Optional[str] = None
    is_active: bool = True
    
    @computed_field
    @property
    def total_slots(self) -> int:
        return self.rows * self.slots_per_row

class PanelTemplateCreate(PanelTemplateBase):
    pass

class PanelTemplateUpdate(BaseModel):
    name: Optional[str] = None
    model: Optional[str] = None
    manufacturer: Optional[str] = None
    series: Optional[str] = None
    rows: Optional[int] = None
    slots_per_row: Optional[int] = None
    voltage: Optional[float] = None
    max_current: Optional[float] = None
    enclosure_type: Optional[str] = None
    protection_rating: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class PanelTemplate(PanelTemplateBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Device Template Schemas
class DeviceTemplateBase(BaseModel):
    name: str
    model: str
    manufacturer: str = "Hager"
    series: Optional[str] = None
    device_type: str  # MCB, RCD, RCBO, Smart Meter
    category: str     # Protection, Measurement, Control
    slots_required: int = 1
    rated_current: Optional[float] = None
    max_current: Optional[float] = None
    voltage_range: Optional[str] = None
    breaking_capacity: Optional[float] = None
    sensitivity: Optional[float] = None
    curve_type: Optional[str] = None
    pole_count: Optional[int] = None
    width_in_modules: float = 1.0
    mounting_type: Optional[str] = None
    features: Optional[str] = None
    description: Optional[str] = None
    is_active: bool = True

class DeviceTemplateCreate(DeviceTemplateBase):
    pass

class DeviceTemplateUpdate(BaseModel):
    name: Optional[str] = None
    model: Optional[str] = None
    manufacturer: Optional[str] = None
    series: Optional[str] = None
    device_type: Optional[str] = None
    category: Optional[str] = None
    slots_required: Optional[int] = None
    rated_current: Optional[float] = None
    max_current: Optional[float] = None
    voltage_range: Optional[str] = None
    breaking_capacity: Optional[float] = None
    sensitivity: Optional[float] = None
    curve_type: Optional[str] = None
    pole_count: Optional[int] = None
    width_in_modules: Optional[float] = None
    mounting_type: Optional[str] = None
    features: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class DeviceTemplate(DeviceTemplateBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Panel Schemas (Updated to use templates)
class PanelBase(BaseModel):
    name: str
    template_id: int
    location: Optional[str] = None
    installation_date: Optional[datetime] = None
    description: Optional[str] = None

class PanelCreate(PanelBase):
    pass

class PanelUpdate(BaseModel):
    name: Optional[str] = None
    template_id: Optional[int] = None
    location: Optional[str] = None
    installation_date: Optional[datetime] = None
    description: Optional[str] = None

class Panel(PanelBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    template: Optional[PanelTemplate] = None
    
    class Config:
        from_attributes = True

# Device Type Schemas (Legacy - to be phased out)
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

# Panel Slot Schemas (Updated to use templates)
class PanelSlotBase(BaseModel):
    slot_number: int
    row: int
    column: int
    device_label: Optional[str] = None
    current_setting: Optional[float] = None
    custom_properties: Optional[str] = None
    spans_slots: int = 1
    installed_date: Optional[datetime] = None

class PanelSlotCreate(PanelSlotBase):
    panel_id: int
    device_template_id: Optional[int] = None

class PanelSlotUpdate(BaseModel):
    device_template_id: Optional[int] = None
    device_label: Optional[str] = None
    current_setting: Optional[float] = None
    custom_properties: Optional[str] = None
    spans_slots: Optional[int] = None
    installed_date: Optional[datetime] = None

class PanelSlot(PanelSlotBase):
    id: int
    panel_id: int
    device_template_id: Optional[int] = None
    is_occupied: bool
    device_template: Optional[DeviceTemplate] = None
    
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

# Template library schemas (for API responses)
class DeviceTemplateWithInstances(DeviceTemplate):
    device_instances: List[PanelSlot] = []
