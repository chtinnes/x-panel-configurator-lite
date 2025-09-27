"""
Device Template Mapper
Converts DigiKey API responses to DeviceTemplate database models
"""

import re
import logging
from typing import Dict, List, Optional, Any
from decimal import Decimal

from models import DeviceTemplate, PanelTemplate
from services.digikey_config import DEVICE_TYPE_MAPPING

logger = logging.getLogger(__name__)


class DeviceTemplateMapper:
    """Maps DigiKey product data to DeviceTemplate models"""
    
    @staticmethod
    def determine_device_type(category: str, description: str) -> str:
        """Determine device type from DigiKey category and description"""
        category_upper = category.upper()
        description_upper = description.upper()
        
        # Check category first
        for digikey_type, device_type in DEVICE_TYPE_MAPPING.items():
            if digikey_type.upper() in category_upper:
                return device_type
        
        # Check description for device type keywords
        if any(keyword in description_upper for keyword in ["RCD", "RESIDUAL CURRENT"]):
            if any(keyword in description_upper for keyword in ["CIRCUIT BREAKER", "RCBO"]):
                return "RCBO"
            else:
                return "RCD"
        elif any(keyword in description_upper for keyword in ["CIRCUIT BREAKER", "MCB", "MINIATURE"]):
            return "MCB"
        elif any(keyword in description_upper for keyword in ["SMART METER", "ENERGY METER"]):
            return "SMART_METER"
        elif any(keyword in description_upper for keyword in ["CONTACTOR"]):
            return "CONTACTOR"
        
        # Default fallback
        return "MCB"
    
    @staticmethod
    def determine_slots_required(device_type: str, pole_count: Optional[int] = None, description: str = "") -> int:
        """Determine number of DIN rail slots required"""
        description_upper = description.upper()
        
        if device_type == "SMART_METER":
            # Smart meters typically require 4 slots
            return 4
        elif device_type == "RCBO":
            # RCBOs typically require 2 slots
            return 2
        elif device_type in ["MCB", "RCD"]:
            # Use pole count if available, otherwise try to extract from description
            if pole_count:
                return pole_count
            
            # Try to extract pole count from description
            for pattern in [r"(\d+)\s*POLE", r"(\d+)P", r"(\d+)\s*WAY"]:
                match = re.search(pattern, description_upper)
                if match:
                    return int(match.group(1))
            
            # Default for single pole MCB/RCD
            return 1
        elif device_type == "CONTACTOR":
            # Contactors vary, use pole count or default to 3 (3-phase)
            return pole_count if pole_count else 3
        
        # Default fallback
        return 1
    
    @staticmethod
    def extract_wire_colors(device_type: str, voltage_rating: Optional[int] = None) -> List[str]:
        """Get appropriate wire colors for device type and voltage"""
        if device_type in ["MCB", "RCBO"] and voltage_rating:
            if voltage_rating <= 230:
                # Single phase: Live, Neutral, Earth
                return ["Brown", "Blue", "Green/Yellow"]
            else:
                # Three phase: L1, L2, L3, Neutral, Earth  
                return ["Brown", "Black", "Grey", "Blue", "Green/Yellow"]
        elif device_type == "RCD":
            # RCD typically has Live, Neutral, Earth
            return ["Brown", "Blue", "Green/Yellow"]
        elif device_type == "CONTACTOR":
            # Three phase contactor
            return ["Brown", "Black", "Grey", "Blue", "Green/Yellow"]
        elif device_type == "SMART_METER":
            # Smart meter connections
            return ["Brown", "Black", "Grey", "Blue", "Green/Yellow"]
        
        # Default single phase colors
        return ["Brown", "Blue", "Green/Yellow"]
    
    @staticmethod
    def extract_wire_cross_sections(current_rating: Optional[int] = None) -> List[str]:
        """Get appropriate wire cross-sections based on current rating"""
        if not current_rating:
            return ["2.5mm²"]
        
        # UK/EU standard wire cross-sections for different current ratings
        if current_rating <= 6:
            return ["1.5mm²"]
        elif current_rating <= 16:
            return ["2.5mm²"]
        elif current_rating <= 20:
            return ["4.0mm²"]
        elif current_rating <= 32:
            return ["6.0mm²"]
        elif current_rating <= 40:
            return ["10.0mm²"]
        elif current_rating <= 50:
            return ["16.0mm²"]
        else:
            return ["25.0mm²"]
    
    @classmethod
    def create_device_template_from_digikey(cls, digikey_specs: Dict[str, Any]) -> DeviceTemplate:
        """Create DeviceTemplate from DigiKey product specifications"""
        
        # Extract basic information
        part_number = digikey_specs.get("part_number", "")
        manufacturer = digikey_specs.get("manufacturer", "")
        description = digikey_specs.get("description", "")
        category = digikey_specs.get("category", "")
        
        # Determine device type
        device_type = cls.determine_device_type(category, description)
        
        # Extract electrical specifications
        current_rating = digikey_specs.get("current_rating")
        voltage_rating = digikey_specs.get("voltage_rating", 230)  # Default to 230V
        pole_count = digikey_specs.get("pole_count")
        
        # Determine physical properties
        slots_required = cls.determine_slots_required(device_type, pole_count, description)
        
        # Generate wire specifications
        wire_colors = cls.extract_wire_colors(device_type, voltage_rating)
        wire_cross_sections = cls.extract_wire_cross_sections(current_rating)
        
        # Create template name
        template_name = f"{manufacturer} {device_type}"
        if current_rating:
            template_name += f" {current_rating}A"
        if voltage_rating != 230:
            template_name += f" {voltage_rating}V"
        
        # Create DeviceTemplate
        device_template = DeviceTemplate(
            name=template_name,
            manufacturer=manufacturer,
            part_number=part_number,
            device_type=device_type,
            current_rating=current_rating,
            voltage_rating=voltage_rating,
            pole_count=pole_count or 1,
            slots_required=slots_required,
            wire_colors=wire_colors,
            wire_cross_sections=wire_cross_sections,
            description=description,
            # Additional fields for tracking
            digikey_part_number=part_number,
            unit_price=digikey_specs.get("unit_price", 0.0),
            currency=digikey_specs.get("currency", "USD"),
            quantity_available=digikey_specs.get("quantity_available", 0)
        )
        
        logger.info(f"Created DeviceTemplate: {template_name}")
        return device_template
    
    @classmethod
    def create_device_templates_from_search(cls, search_results: List[Dict[str, Any]]) -> List[DeviceTemplate]:
        """Create multiple DeviceTemplates from DigiKey search results"""
        templates = []
        
        for product_specs in search_results:
            try:
                template = cls.create_device_template_from_digikey(product_specs)
                templates.append(template)
            except Exception as e:
                logger.error(f"Failed to create template for {product_specs.get('part_number', 'unknown')}: {e}")
                continue
        
        logger.info(f"Created {len(templates)} device templates from {len(search_results)} search results")
        return templates


class PanelTemplateMapper:
    """Maps panel specifications to PanelTemplate models"""
    
    @classmethod
    def create_hager_panel_templates(cls) -> List[PanelTemplate]:
        """Create standard Hager Volta panel templates"""
        
        hager_panels = [
            {
                "name": "Hager Volta VML306 6-Way",
                "manufacturer": "Hager",
                "series": "Volta",
                "model_number": "VML306",
                "slot_count": 6,
                "mounting_type": "Surface Mount",
                "ip_rating": "IP30",
                "dimensions": "192mm x 144mm x 85mm",
                "description": "6-way consumer unit with 100A main switch"
            },
            {
                "name": "Hager Volta VML912 12-Way",
                "manufacturer": "Hager",
                "series": "Volta",
                "model_number": "VML912", 
                "slot_count": 12,
                "mounting_type": "Surface Mount",
                "ip_rating": "IP30",
                "dimensions": "264mm x 144mm x 85mm",
                "description": "12-way consumer unit with 100A main switch"
            },
            {
                "name": "Hager Volta VML918 18-Way",
                "manufacturer": "Hager",
                "series": "Volta",
                "model_number": "VML918",
                "slot_count": 18,
                "mounting_type": "Surface Mount", 
                "ip_rating": "IP30",
                "dimensions": "336mm x 144mm x 85mm",
                "description": "18-way consumer unit with 100A main switch"
            },
            {
                "name": "Hager Volta VML924 24-Way",
                "manufacturer": "Hager",
                "series": "Volta",
                "model_number": "VML924",
                "slot_count": 24,
                "mounting_type": "Surface Mount",
                "ip_rating": "IP30", 
                "dimensions": "408mm x 144mm x 85mm",
                "description": "24-way consumer unit with 100A main switch"
            }
        ]
        
        templates = []
        for panel_data in hager_panels:
            template = PanelTemplate(
                name=panel_data["name"],
                manufacturer=panel_data["manufacturer"],
                series=panel_data["series"],
                model=panel_data["model_number"],
                rows=2,  # Standard 2-row panel
                slots_per_row=panel_data["slot_count"] // 2,
                voltage=230,  # Standard UK voltage
                max_current=100,  # Standard 100A
                enclosure_type=panel_data["mounting_type"],
                protection_rating=panel_data["ip_rating"],
                description=panel_data["description"]
            )
            templates.append(template)
        
        logger.info(f"Created {len(templates)} Hager panel templates")
        return templates