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

def can_place_device_at_slot(db: Session, slot_id: int, device_type_id: int) -> bool:
    """Check if a device can be placed at the given slot"""
    # Get the slot and device type
    slot = db.query(PanelSlot).filter(PanelSlot.id == slot_id).first()
    if not slot:
        return False
    
    device_type = db.query(DeviceType).filter(DeviceType.id == device_type_id).first()
    if not device_type:
        return False
    
    slots_required = device_type.slots_required
    
    # For single slot devices, just check if current slot is free
    if slots_required == 1:
        return not slot.is_occupied
    
    # For multi-slot devices, check consecutive slots in the same row
    panel_slots = db.query(PanelSlot).filter(
        PanelSlot.panel_id == slot.panel_id,
        PanelSlot.row == slot.row
    ).order_by(PanelSlot.column).all()
    
    # Find the starting slot index in its row
    slot_index = None
    for i, s in enumerate(panel_slots):
        if s.id == slot_id:
            slot_index = i
            break
    
    if slot_index is None:
        return False
    
    # Check if we have enough consecutive free slots
    if slot_index + slots_required > len(panel_slots):
        return False
    
    # Check if all required slots are free
    for i in range(slot_index, slot_index + slots_required):
        if panel_slots[i].is_occupied:
            return False
    
    return True

@router.put("/slots/{slot_id}", response_model=PanelSlotSchema)
def update_panel_slot(slot_id: int, slot_update: PanelSlotUpdate, db: Session = Depends(get_db)):
    """Update a panel slot with a device"""
    db_slot = db.query(PanelSlot).filter(PanelSlot.id == slot_id).first()
    if not db_slot:
        raise HTTPException(status_code=404, detail="Panel slot not found")
    
    # If placing a device, check if it can be placed
    if slot_update.device_type_id is not None:
        # Get device type to check slot requirements
        device_type = db.query(DeviceType).filter(DeviceType.id == slot_update.device_type_id).first()
        if not device_type:
            raise HTTPException(status_code=404, detail="Device type not found")
        
        # Check if enough consecutive slots are available
        if not can_place_device_at_slot(db, slot_id, slot_update.device_type_id):
            raise HTTPException(status_code=400, detail="Cannot place device at this slot - not enough consecutive free slots")
        
        # Remove any existing device from this slot first (clean up any multi-slot device)
        remove_device_from_slot(slot_id, db)
        
        # Update the primary slot with device information
        for field, value in slot_update.dict(exclude_unset=True).items():
            if hasattr(db_slot, field):
                setattr(db_slot, field, value)
        
        db_slot.is_occupied = True
        db_slot.spans_slots = device_type.slots_required
        
        # If device spans multiple slots, mark additional slots as occupied
        if device_type.slots_required > 1:
            # Get all slots in the same row
            panel_slots = db.query(PanelSlot).filter(
                PanelSlot.panel_id == db_slot.panel_id,
                PanelSlot.row == db_slot.row
            ).order_by(PanelSlot.column).all()
            
            # Find starting slot index
            slot_index = None
            for i, s in enumerate(panel_slots):
                if s.id == slot_id:
                    slot_index = i
                    break
            
            if slot_index is not None:
                # Mark additional slots as occupied (but not configured)
                for i in range(slot_index + 1, min(slot_index + device_type.slots_required, len(panel_slots))):
                    additional_slot = panel_slots[i]
                    additional_slot.is_occupied = True
                    additional_slot.device_type_id = None  # Only the primary slot has the device reference
                    additional_slot.spans_slots = 0  # Indicate this is a secondary slot
        
    else:
        # Just removing a device
        remove_device_from_slot(slot_id, db)
    
    db.commit()
    db.refresh(db_slot)
    return db_slot

@router.delete("/slots/{slot_id}/device")
def remove_device_from_slot(slot_id: int, db: Session = Depends(get_db)):
    """Remove device from a panel slot and free up all spanned slots"""
    db_slot = db.query(PanelSlot).filter(PanelSlot.id == slot_id).first()
    if not db_slot:
        raise HTTPException(status_code=404, detail="Panel slot not found")
    
    # If this slot spans multiple slots, we need to free them all
    if db_slot.is_occupied and db_slot.spans_slots > 1:
        # Get all slots in the same row
        panel_slots = db.query(PanelSlot).filter(
            PanelSlot.panel_id == db_slot.panel_id,
            PanelSlot.row == db_slot.row
        ).order_by(PanelSlot.column).all()
        
        # Find starting slot index
        slot_index = None
        for i, s in enumerate(panel_slots):
            if s.id == slot_id:
                slot_index = i
                break
        
        if slot_index is not None:
            # Clear all spanned slots
            for i in range(slot_index, min(slot_index + db_slot.spans_slots, len(panel_slots))):
                slot_to_clear = panel_slots[i]
                slot_to_clear.device_type_id = None
                slot_to_clear.device_label = None
                slot_to_clear.current_setting = None
                slot_to_clear.is_occupied = False
                slot_to_clear.spans_slots = 1
    else:
        # Single slot device or already cleared
        db_slot.device_type_id = None
        db_slot.device_label = None
        db_slot.current_setting = None
        db_slot.is_occupied = False
        db_slot.spans_slots = 1
    
    db.commit()
    return {"message": "Device removed from slot"}

@router.get("/slots/{slot_id}/can-place/{device_type_id}")
def check_device_placement(slot_id: int, device_type_id: int, db: Session = Depends(get_db)):
    """Check if a device can be placed at a specific slot"""
    can_place = can_place_device_at_slot(db, slot_id, device_type_id)
    
    # Get additional info for debugging
    slot = db.query(PanelSlot).filter(PanelSlot.id == slot_id).first()
    device_type = db.query(DeviceType).filter(DeviceType.id == device_type_id).first()
    
    return {
        "can_place": can_place,
        "slot_info": {
            "id": slot.id if slot else None,
            "row": slot.row if slot else None,
            "column": slot.column if slot else None,
            "is_occupied": slot.is_occupied if slot else None,
            "spans_slots": slot.spans_slots if slot else None
        },
        "device_info": {
            "id": device_type.id if device_type else None,
            "name": device_type.name if device_type else None,
            "slots_required": device_type.slots_required if device_type else None
        }
    }

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