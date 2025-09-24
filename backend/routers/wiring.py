from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Wire, Panel, PanelSlot
from schemas import Wire as WireSchema, WireCreate, WireUpdate

router = APIRouter()

@router.get("/panel/{panel_id}", response_model=List[WireSchema])
def get_panel_wiring(panel_id: int, db: Session = Depends(get_db)):
    """Get all wiring for a specific panel"""
    panel = db.query(Panel).filter(Panel.id == panel_id).first()
    if not panel:
        raise HTTPException(status_code=404, detail="Panel not found")
    
    wires = db.query(Wire).filter(Wire.panel_id == panel_id).all()
    return wires

@router.get("/{wire_id}", response_model=WireSchema)
def get_wire(wire_id: int, db: Session = Depends(get_db)):
    """Get a specific wire"""
    wire = db.query(Wire).filter(Wire.id == wire_id).first()
    if not wire:
        raise HTTPException(status_code=404, detail="Wire not found")
    return wire

@router.post("/", response_model=WireSchema)
def create_wire(wire: WireCreate, db: Session = Depends(get_db)):
    """Create a new wire connection"""
    # Validate panel exists
    panel = db.query(Panel).filter(Panel.id == wire.panel_id).first()
    if not panel:
        raise HTTPException(status_code=404, detail="Panel not found")
    
    # Validate slots exist if specified
    if wire.source_slot_id:
        source_slot = db.query(PanelSlot).filter(PanelSlot.id == wire.source_slot_id).first()
        if not source_slot:
            raise HTTPException(status_code=404, detail="Source slot not found")
    
    if wire.destination_slot_id:
        dest_slot = db.query(PanelSlot).filter(PanelSlot.id == wire.destination_slot_id).first()
        if not dest_slot:
            raise HTTPException(status_code=404, detail="Destination slot not found")
    
    db_wire = Wire(**wire.dict())
    db.add(db_wire)
    db.commit()
    db.refresh(db_wire)
    return db_wire

@router.put("/{wire_id}", response_model=WireSchema)
def update_wire(wire_id: int, wire_update: WireUpdate, db: Session = Depends(get_db)):
    """Update a wire connection"""
    db_wire = db.query(Wire).filter(Wire.id == wire_id).first()
    if not db_wire:
        raise HTTPException(status_code=404, detail="Wire not found")
    
    for field, value in wire_update.dict(exclude_unset=True).items():
        setattr(db_wire, field, value)
    
    db.commit()
    db.refresh(db_wire)
    return db_wire

@router.delete("/{wire_id}")
def delete_wire(wire_id: int, db: Session = Depends(get_db)):
    """Delete a wire connection"""
    db_wire = db.query(Wire).filter(Wire.id == wire_id).first()
    if not db_wire:
        raise HTTPException(status_code=404, detail="Wire not found")
    
    db.delete(db_wire)
    db.commit()
    return {"message": "Wire deleted successfully"}

@router.get("/standards/colors")
def get_wire_color_standards():
    """Get standard wire colors for different types"""
    standards = {
        "UK": {
            "Live": ["Brown", "Black", "Grey"],
            "Neutral": ["Blue"],
            "Earth": ["Green/Yellow"],
            "Switched Live": ["Brown", "Black", "Grey"]
        },
        "EU": {
            "Live": ["Brown", "Black", "Grey"], 
            "Neutral": ["Blue"],
            "Earth": ["Green/Yellow"],
            "Switched Live": ["Brown", "Black", "Grey"]
        }
    }
    return standards

@router.get("/standards/cross-sections")
def get_wire_cross_section_standards():
    """Get standard wire cross-sections for different currents"""
    standards = {
        "domestic": [
            {"current": "6A", "cross_section": 1.0, "typical_use": "Lighting circuits"},
            {"current": "10A", "cross_section": 1.5, "typical_use": "Lighting circuits"},
            {"current": "16A", "cross_section": 2.5, "typical_use": "Socket outlets"},
            {"current": "20A", "cross_section": 2.5, "typical_use": "Socket outlets, small appliances"},
            {"current": "25A", "cross_section": 4.0, "typical_use": "Kitchen appliances"},
            {"current": "32A", "cross_section": 6.0, "typical_use": "Cooker, large appliances"},
            {"current": "40A", "cross_section": 10.0, "typical_use": "Electric shower, main feeds"},
            {"current": "50A", "cross_section": 16.0, "typical_use": "Main incoming supply"}
        ]
    }
    return standards
