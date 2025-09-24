from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import DeviceType, PanelSlot
from schemas import DeviceType as DeviceTypeSchema, DeviceTypeCreate, PanelSlot as PanelSlotSchema, PanelSlotUpdate

router = APIRouter()

@router.get("/types", response_model=List[DeviceTypeSchema])
def get_device_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all device types"""
    device_types = db.query(DeviceType).offset(skip).limit(limit).all()
    return device_types

@router.get("/types/{device_type_id}", response_model=DeviceTypeSchema)
def get_device_type(device_type_id: int, db: Session = Depends(get_db)):
    """Get a specific device type"""
    device_type = db.query(DeviceType).filter(DeviceType.id == device_type_id).first()
    if not device_type:
        raise HTTPException(status_code=404, detail="Device type not found")
    return device_type

@router.post("/types", response_model=DeviceTypeSchema)
def create_device_type(device_type: DeviceTypeCreate, db: Session = Depends(get_db)):
    """Create a new device type"""
    db_device_type = DeviceType(**device_type.dict())
    db.add(db_device_type)
    db.commit()
    db.refresh(db_device_type)
    return db_device_type

@router.put("/slots/{slot_id}", response_model=PanelSlotSchema)
def update_panel_slot(slot_id: int, slot_update: PanelSlotUpdate, db: Session = Depends(get_db)):
    """Update a panel slot with a device"""
    db_slot = db.query(PanelSlot).filter(PanelSlot.id == slot_id).first()
    if not db_slot:
        raise HTTPException(status_code=404, detail="Panel slot not found")
    
    # Update slot properties
    for field, value in slot_update.dict(exclude_unset=True).items():
        setattr(db_slot, field, value)
    
    # Update occupation status
    db_slot.is_occupied = db_slot.device_type_id is not None
    
    db.commit()
    db.refresh(db_slot)
    return db_slot

@router.delete("/slots/{slot_id}/device")
def remove_device_from_slot(slot_id: int, db: Session = Depends(get_db)):
    """Remove device from a panel slot"""
    db_slot = db.query(PanelSlot).filter(PanelSlot.id == slot_id).first()
    if not db_slot:
        raise HTTPException(status_code=404, detail="Panel slot not found")
    
    db_slot.device_type_id = None
    db_slot.device_label = None
    db_slot.current_setting = None
    db_slot.is_occupied = False
    db_slot.spans_slots = 1
    
    db.commit()
    return {"message": "Device removed from slot"}

@router.get("/library/hager")
def get_hager_device_library():
    """Get predefined Hager device library"""
    devices = [
        {
            "id": 1,
            "name": "MCB 6A Type B",
            "category": "Protection",
            "manufacturer": "Hager",
            "model": "MBN106",
            "slots_required": 1,
            "max_current": 6.0,
            "voltage_range": "230V",
            "description": "6A Type B Miniature Circuit Breaker"
        },
        {
            "id": 2,
            "name": "MCB 10A Type B", 
            "category": "Protection",
            "manufacturer": "Hager",
            "model": "MBN110",
            "slots_required": 1,
            "max_current": 10.0,
            "voltage_range": "230V",
            "description": "10A Type B Miniature Circuit Breaker"
        },
        {
            "id": 3,
            "name": "MCB 16A Type B",
            "category": "Protection", 
            "manufacturer": "Hager",
            "model": "MBN116",
            "slots_required": 1,
            "max_current": 16.0,
            "voltage_range": "230V",
            "description": "16A Type B Miniature Circuit Breaker"
        },
        {
            "id": 4,
            "name": "MCB 20A Type B",
            "category": "Protection",
            "manufacturer": "Hager",
            "model": "MBN120", 
            "slots_required": 1,
            "max_current": 20.0,
            "voltage_range": "230V",
            "description": "20A Type B Miniature Circuit Breaker"
        },
        {
            "id": 5,
            "name": "MCB 32A Type B",
            "category": "Protection",
            "manufacturer": "Hager",
            "model": "MBN132",
            "slots_required": 1,
            "max_current": 32.0,
            "voltage_range": "230V",
            "description": "32A Type B Miniature Circuit Breaker"
        },
        {
            "id": 6,
            "name": "RCBO 16A Type B 30mA",
            "category": "Protection",
            "manufacturer": "Hager",
            "model": "ADA116G",
            "slots_required": 2,
            "max_current": 16.0,
            "voltage_range": "230V",
            "description": "16A Type B RCBO with 30mA RCD protection"
        },
        {
            "id": 7,
            "name": "RCBO 20A Type B 30mA",
            "category": "Protection", 
            "manufacturer": "Hager",
            "model": "ADA120G",
            "slots_required": 2,
            "max_current": 20.0,
            "voltage_range": "230V",
            "description": "20A Type B RCBO with 30mA RCD protection"
        },
        {
            "id": 8,
            "name": "RCD 63A 30mA",
            "category": "Protection",
            "manufacturer": "Hager",
            "model": "CDC263D",
            "slots_required": 2,
            "max_current": 63.0,
            "voltage_range": "230V",
            "description": "63A 30mA RCD for overall protection"
        },
        {
            "id": 9,
            "name": "Smart Meter Interface",
            "category": "Measurement",
            "manufacturer": "Hager",
            "model": "EHZ361Z5",
            "slots_required": 4,
            "max_current": 80.0,
            "voltage_range": "230V",
            "description": "Smart electricity meter with digital interface"
        },
        {
            "id": 10,
            "name": "Contactor 25A",
            "category": "Control",
            "manufacturer": "Hager",
            "model": "ERC225",
            "slots_required": 2,
            "max_current": 25.0,
            "voltage_range": "230V",
            "description": "25A modular contactor for switching loads"
        }
    ]
    return devices