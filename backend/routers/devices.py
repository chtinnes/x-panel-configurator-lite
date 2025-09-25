from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import DeviceTemplate, PanelSlot
from schemas import PanelSlot as PanelSlotSchema, PanelSlotUpdate

router = APIRouter()

def can_place_device_at_slot(db: Session, slot_id: int, device_template_id: int) -> bool:
    """Check if a device can be placed at the given slot"""
    # Get the slot and device template
    slot = db.query(PanelSlot).filter(PanelSlot.id == slot_id).first()
    if not slot:
        return False
    
    device_template = db.query(DeviceTemplate).filter(DeviceTemplate.id == device_template_id).first()
    if not device_template:
        return False
    
    slots_required = getattr(device_template, 'slots_required', 1)
    
    # For single slot devices, just check if current slot is free
    if slots_required == 1:
        return not getattr(slot, 'is_occupied', True)
    
    # For multi-slot devices, check consecutive slots in the same row
    panel_slots = db.query(PanelSlot).filter(
        PanelSlot.panel_id == slot.panel_id,
        PanelSlot.row == slot.row
    ).order_by(PanelSlot.column).all()
    
    # Find the starting slot index in its row
    slot_index = None
    for i, s in enumerate(panel_slots):
        if getattr(s, 'id', None) == slot_id:
            slot_index = i
            break
    
    if slot_index is None:
        return False
    
    # Check if we have enough consecutive free slots
    if slot_index + slots_required > len(panel_slots):
        return False
    
    # Check if all required slots are free
    for i in range(slot_index, slot_index + slots_required):
        if getattr(panel_slots[i], 'is_occupied', True):
            return False
    
    return True

@router.put("/slots/{slot_id}", response_model=PanelSlotSchema)
def update_panel_slot(slot_id: int, slot_update: PanelSlotUpdate, db: Session = Depends(get_db)):
    """Update a panel slot with a device"""
    db_slot = db.query(PanelSlot).filter(PanelSlot.id == slot_id).first()
    if not db_slot:
        raise HTTPException(status_code=404, detail="Panel slot not found")
    
    # If placing a device, check if it can be placed
    if slot_update.device_template_id is not None:
        # Get device template to check slot requirements
        device_template = db.query(DeviceTemplate).filter(DeviceTemplate.id == slot_update.device_template_id).first()
        if not device_template:
            raise HTTPException(status_code=404, detail="Device template not found")
        
        # Check if this is updating an existing device (same device template) or placing a new one
        current_template_id = getattr(db_slot, 'device_template_id', None)
        is_same_device = (current_template_id is not None and 
                         current_template_id == slot_update.device_template_id)
        
        # Only check slot availability for new device placements, not when updating properties of existing devices
        if not is_same_device:
            # Check if enough consecutive slots are available
            if not can_place_device_at_slot(db, slot_id, slot_update.device_template_id):
                raise HTTPException(status_code=400, detail="Cannot place device at this slot - not enough consecutive free slots")
            
            # Remove any existing device from this slot first (clean up any multi-slot device)
            remove_device_from_slot(slot_id, db)
        
        # Update the primary slot with device information
        for field, value in slot_update.model_dump(exclude_unset=True).items():
            if hasattr(db_slot, field):
                setattr(db_slot, field, value)
        
        # Only update occupation and slot spanning for new device placements
        if not is_same_device:
            setattr(db_slot, 'is_occupied', True)
            setattr(db_slot, 'spans_slots', device_template.slots_required)
        
        # If device spans multiple slots, mark additional slots as occupied
        slots_required = getattr(device_template, 'slots_required', 1)
        if slots_required > 1:
            # Get all slots in the same row
            panel_slots = db.query(PanelSlot).filter(
                PanelSlot.panel_id == db_slot.panel_id,
                PanelSlot.row == db_slot.row
            ).order_by(PanelSlot.column).all()
            
            # Find starting slot index
            slot_index = None
            for i, s in enumerate(panel_slots):
                if getattr(s, 'id', None) == slot_id:
                    slot_index = i
                    break
            
            if slot_index is not None:
                # Mark additional slots as occupied (but not configured)
                for i in range(slot_index + 1, min(slot_index + slots_required, len(panel_slots))):
                    additional_slot = panel_slots[i]
                    setattr(additional_slot, 'is_occupied', True)
                    setattr(additional_slot, 'device_template_id', None)
                    setattr(additional_slot, 'spans_slots', 0)
        
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
    is_occupied = getattr(db_slot, 'is_occupied', False)
    spans_slots = getattr(db_slot, 'spans_slots', 1)
    
    if is_occupied and spans_slots > 1:
        # Get all slots in the same row
        panel_slots = db.query(PanelSlot).filter(
            PanelSlot.panel_id == db_slot.panel_id,
            PanelSlot.row == db_slot.row
        ).order_by(PanelSlot.column).all()
        
        # Find starting slot index
        slot_index = None
        for i, s in enumerate(panel_slots):
            if getattr(s, 'id', None) == slot_id:
                slot_index = i
                break
        
        if slot_index is not None:
            # Clear all spanned slots
            for i in range(slot_index, min(slot_index + spans_slots, len(panel_slots))):
                slot_to_clear = panel_slots[i]
                setattr(slot_to_clear, 'device_template_id', None)
                setattr(slot_to_clear, 'device_label', None)
                setattr(slot_to_clear, 'current_setting', None)
                setattr(slot_to_clear, 'is_occupied', False)
                setattr(slot_to_clear, 'spans_slots', 1)
    else:
        # Single slot device or already cleared
        setattr(db_slot, 'device_template_id', None)
        setattr(db_slot, 'device_label', None)
        setattr(db_slot, 'current_setting', None)
        setattr(db_slot, 'is_occupied', False)
        setattr(db_slot, 'spans_slots', 1)
    
    db.commit()
    return {"message": "Device removed from slot"}

@router.get("/slots/{slot_id}/can-place/{device_template_id}")
def check_device_placement(slot_id: int, device_template_id: int, db: Session = Depends(get_db)):
    """Check if a device can be placed at a specific slot"""
    can_place = can_place_device_at_slot(db, slot_id, device_template_id)
    
    # Get additional info for debugging
    slot = db.query(PanelSlot).filter(PanelSlot.id == slot_id).first()
    device_template = db.query(DeviceTemplate).filter(DeviceTemplate.id == device_template_id).first()
    
    return {
        "can_place": can_place,
        "slot_info": {
            "id": getattr(slot, 'id', None),
            "row": getattr(slot, 'row', None),
            "column": getattr(slot, 'column', None),
            "is_occupied": getattr(slot, 'is_occupied', None),
            "spans_slots": getattr(slot, 'spans_slots', None)
        },
        "device_info": {
            "id": getattr(device_template, 'id', None),
            "name": getattr(device_template, 'name', None),
            "slots_required": getattr(device_template, 'slots_required', None)
        }
    }

@router.get("/library/hager")
def get_hager_device_library():
    """Redirect to template-based device library - DEPRECATED"""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/api/templates/library/devices/hager", status_code=301)