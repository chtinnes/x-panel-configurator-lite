from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import PanelTemplate, DeviceTemplate
from schemas import (
    PanelTemplate as PanelTemplateSchema,
    PanelTemplateCreate,
    PanelTemplateUpdate,
    DeviceTemplate as DeviceTemplateSchema,
    DeviceTemplateCreate,
    DeviceTemplateUpdate,
    DeviceTemplateWithInstances
)

router = APIRouter()

# Panel Template endpoints
@router.get("/panel-templates", response_model=List[PanelTemplateSchema])
def get_panel_templates(
    manufacturer: Optional[str] = None,
    series: Optional[str] = None,
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    """Get all panel templates with optional filtering"""
    query = db.query(PanelTemplate)
    
    if active_only:
        query = query.filter(PanelTemplate.is_active == True)
    
    if manufacturer:
        query = query.filter(PanelTemplate.manufacturer.ilike(f"%{manufacturer}%"))
    
    if series:
        query = query.filter(PanelTemplate.series.ilike(f"%{series}%"))
    
    return query.all()

@router.get("/panel-templates/{template_id}", response_model=PanelTemplateSchema)
def get_panel_template(template_id: int, db: Session = Depends(get_db)):
    """Get a specific panel template by ID"""
    template = db.query(PanelTemplate).filter(PanelTemplate.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Panel template not found")
    return template

@router.post("/panel-templates", response_model=PanelTemplateSchema)
def create_panel_template(template: PanelTemplateCreate, db: Session = Depends(get_db)):
    """Create a new panel template"""
    db_template = PanelTemplate(**template.model_dump())
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    return db_template

@router.put("/panel-templates/{template_id}", response_model=PanelTemplateSchema)
def update_panel_template(
    template_id: int, 
    template: PanelTemplateUpdate, 
    db: Session = Depends(get_db)
):
    """Update a panel template"""
    db_template = db.query(PanelTemplate).filter(PanelTemplate.id == template_id).first()
    if not db_template:
        raise HTTPException(status_code=404, detail="Panel template not found")
    
    update_data = template.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_template, field, value)
    
    db.commit()
    db.refresh(db_template)
    return db_template

@router.delete("/panel-templates/{template_id}")
def delete_panel_template(template_id: int, db: Session = Depends(get_db)):
    """Soft delete a panel template (mark as inactive)"""
    db_template = db.query(PanelTemplate).filter(PanelTemplate.id == template_id).first()
    if not db_template:
        raise HTTPException(status_code=404, detail="Panel template not found")
    
    setattr(db_template, 'is_active', False)
    db.commit()
    return {"message": "Panel template deactivated"}

# Device Template endpoints
@router.get("/device-templates", response_model=List[DeviceTemplateSchema])
def get_device_templates(
    manufacturer: Optional[str] = None,
    series: Optional[str] = None,
    device_type: Optional[str] = None,
    category: Optional[str] = None,
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    """Get all device templates with optional filtering"""
    query = db.query(DeviceTemplate)
    
    if active_only:
        query = query.filter(DeviceTemplate.is_active == True)
    
    if manufacturer:
        query = query.filter(DeviceTemplate.manufacturer.ilike(f"%{manufacturer}%"))
    
    if series:
        query = query.filter(DeviceTemplate.series.ilike(f"%{series}%"))
    
    if device_type:
        query = query.filter(DeviceTemplate.device_type.ilike(f"%{device_type}%"))
    
    if category:
        query = query.filter(DeviceTemplate.category.ilike(f"%{category}%"))
    
    return query.all()

@router.get("/device-templates/{template_id}", response_model=DeviceTemplateSchema)
def get_device_template(template_id: int, db: Session = Depends(get_db)):
    """Get a specific device template by ID"""
    template = db.query(DeviceTemplate).filter(DeviceTemplate.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Device template not found")
    return template

@router.post("/device-templates", response_model=DeviceTemplateSchema)
def create_device_template(template: DeviceTemplateCreate, db: Session = Depends(get_db)):
    """Create a new device template"""
    db_template = DeviceTemplate(**template.model_dump())
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    return db_template

@router.put("/device-templates/{template_id}", response_model=DeviceTemplateSchema)
def update_device_template(
    template_id: int, 
    template: DeviceTemplateUpdate, 
    db: Session = Depends(get_db)
):
    """Update a device template"""
    db_template = db.query(DeviceTemplate).filter(DeviceTemplate.id == template_id).first()
    if not db_template:
        raise HTTPException(status_code=404, detail="Device template not found")
    
    update_data = template.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_template, field, value)
    
    db.commit()
    db.refresh(db_template)
    return db_template

@router.delete("/device-templates/{template_id}")
def delete_device_template(template_id: int, db: Session = Depends(get_db)):
    """Soft delete a device template (mark as inactive)"""
    db_template = db.query(DeviceTemplate).filter(DeviceTemplate.id == template_id).first()
    if not db_template:
        raise HTTPException(status_code=404, detail="Device template not found")
    
    setattr(db_template, 'is_active', False)
    db.commit()
    return {"message": "Device template deactivated"}

# Library endpoint - replaces the old device library
@router.get("/library/devices/{manufacturer}", response_model=List[DeviceTemplateSchema])
def get_device_library(
    manufacturer: str = "hager",
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get device templates for the component library"""
    query = db.query(DeviceTemplate).filter(
        DeviceTemplate.manufacturer.ilike(f"%{manufacturer}%"),
        DeviceTemplate.is_active == True
    )
    
    if category:
        query = query.filter(DeviceTemplate.category.ilike(f"%{category}%"))
    
    # Order by category and name for consistent display
    query = query.order_by(DeviceTemplate.category, DeviceTemplate.name)
    
    return query.all()

@router.get("/library/panels/{manufacturer}", response_model=List[PanelTemplateSchema])
def get_panel_library(
    manufacturer: str = "hager",
    series: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get panel templates for the component library"""
    query = db.query(PanelTemplate).filter(
        PanelTemplate.manufacturer.ilike(f"%{manufacturer}%"),
        PanelTemplate.is_active == True
    )
    
    if series:
        query = query.filter(PanelTemplate.series.ilike(f"%{series}%"))
    
    # Order by series and slots for consistent display
    query = query.order_by(PanelTemplate.series, PanelTemplate.total_slots)
    
    return query.all()