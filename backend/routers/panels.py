from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Panel, PanelSlot
from schemas import Panel as PanelSchema, PanelCreate, PanelUpdate, PanelWithSlots

router = APIRouter()

@router.get("/", response_model=List[PanelSchema])
def get_panels(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all panels"""
    panels = db.query(Panel).offset(skip).limit(limit).all()
    return panels

@router.get("/{panel_id}", response_model=PanelWithSlots)
def get_panel(panel_id: int, db: Session = Depends(get_db)):
    """Get a specific panel with its slots"""
    panel = db.query(Panel).filter(Panel.id == panel_id).first()
    if not panel:
        raise HTTPException(status_code=404, detail="Panel not found")
    return panel

@router.post("/", response_model=PanelSchema)
def create_panel(panel: PanelCreate, db: Session = Depends(get_db)):
    """Create a new panel"""
    # Exclude total_slots from dict since it's a computed property
    panel_data = panel.dict(exclude={'total_slots'})
    db_panel = Panel(**panel_data)
    db.add(db_panel)
    db.commit()
    db.refresh(db_panel)
    
    # Create empty slots for the panel organized by rows
    slot_number = 1
    total_slots = panel.rows * panel.slots_per_row
    
    for row in range(1, panel.rows + 1):
        for col in range(1, panel.slots_per_row + 1):
            if slot_number <= total_slots:
                slot = PanelSlot(
                    panel_id=db_panel.id,
                    slot_number=slot_number,
                    row=row,
                    column=col,
                    is_occupied=False
                )
                db.add(slot)
                slot_number += 1
    
    db.commit()
    return db_panel

@router.put("/{panel_id}", response_model=PanelSchema)
def update_panel(panel_id: int, panel_update: PanelUpdate, db: Session = Depends(get_db)):
    """Update a panel"""
    db_panel = db.query(Panel).filter(Panel.id == panel_id).first()
    if not db_panel:
        raise HTTPException(status_code=404, detail="Panel not found")
    
    for field, value in panel_update.dict(exclude_unset=True).items():
        setattr(db_panel, field, value)
    
    db.commit()
    db.refresh(db_panel)
    return db_panel

@router.delete("/{panel_id}")
def delete_panel(panel_id: int, db: Session = Depends(get_db)):
    """Delete a panel"""
    db_panel = db.query(Panel).filter(Panel.id == panel_id).first()
    if not db_panel:
        raise HTTPException(status_code=404, detail="Panel not found")
    
    db.delete(db_panel)
    db.commit()
    return {"message": "Panel deleted successfully"}

@router.get("/templates/hager-volta")
def get_hager_volta_templates():
    """Get predefined Hager Volta panel templates"""
    templates = [
        {
            "name": "Hager Volta 12 Way",
            "model": "VD112",
            "manufacturer": "Hager",
            "rows": 2,
            "slots_per_row": 6,
            "voltage": 230.0,
            "current_rating": 63.0,
            "description": "12-way consumer unit suitable for small to medium homes - 2 rows of 6 slots each"
        },
        {
            "name": "Hager Volta 18 Way",
            "model": "VD118",
            "manufacturer": "Hager", 
            "rows": 2,
            "slots_per_row": 9,
            "voltage": 230.0,
            "current_rating": 100.0,
            "description": "18-way consumer unit suitable for medium to large homes - 2 rows of 9 slots each"
        },
        {
            "name": "Hager Volta 24 Way",
            "model": "VD124",
            "manufacturer": "Hager",
            "rows": 3,
            "slots_per_row": 8,
            "voltage": 230.0,
            "current_rating": 100.0,
            "description": "24-way consumer unit suitable for large homes or small commercial - 3 rows of 8 slots each"
        }
    ]
    return templates
