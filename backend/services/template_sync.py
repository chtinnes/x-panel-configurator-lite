"""
Template Synchronization Service
Orchestrates fetching components from DigiKey API and updating database templates
"""

import logging
from typing import Dict, List, Optional, Set, Any, Union
from datetime import datetime
from sqlalchemy.orm import Session

from services.digikey_client import DigiKeyAPIClient
from services.template_mapper import DeviceTemplateMapper, PanelTemplateMapper
from database import get_db
from models import DeviceTemplate, PanelTemplate

logger = logging.getLogger(__name__)


class TemplateSyncService:
    """Service for synchronizing device templates with DigiKey API"""
    
    def __init__(self, digikey_client: DigiKeyAPIClient):
        self.digikey_client = digikey_client
        self.mapper = DeviceTemplateMapper()
        self.sync_stats = {
            "new_templates": 0,
            "updated_templates": 0,
            "errors": 0,
            "last_sync": None
        }
    
    def sync_manufacturer_components(self, manufacturer: str, component_types: Optional[List[str]] = None, db: Optional[Session] = None) -> Dict[str, Union[int, str, List[str]]]:
        """Sync components for a specific manufacturer"""
        if not self.digikey_client.is_configured():
            logger.error("DigiKey API not configured. Please set DIGIKEY_CLIENT_ID and DIGIKEY_CLIENT_SECRET")
            return {"error": "API not configured"}
        
        if not self.digikey_client.access_token:
            logger.error("DigiKey API not authenticated. Please authenticate first.")
            return {"error": "Not authenticated"}
        
        if db is None:
            db = next(get_db())
        
        if component_types is None:
            component_types = ["circuit_breakers", "rcd_devices", "rcbo_devices", "smart_meters"]
        
        results = {
            "manufacturer": manufacturer,
            "new_templates": 0,
            "updated_templates": 0,
            "errors": 0,
            "component_types": component_types
        }
        
        logger.info(f"Starting sync for {manufacturer} components: {component_types}")
        
        for component_type in component_types:
            try:
                # Search for components of this type
                products = self.digikey_client.search_electrical_components(
                    component_type=component_type,
                    manufacturer=manufacturer,
                    limit=20  # Limit per component type to stay within rate limits
                )
                
                if not products:
                    logger.info(f"No {component_type} products found for {manufacturer}")
                    continue
                
                # Extract specifications from each product
                component_specs = []
                for product in products:
                    specs = self.digikey_client.extract_specifications(product)
                    component_specs.append(specs)
                
                # Create device templates
                new_templates = self.mapper.create_device_templates_from_search(component_specs)
                
                # Save to database
                for template in new_templates:
                    existing_template = db.query(DeviceTemplate).filter(
                        DeviceTemplate.part_number == template.part_number
                    ).first()
                    
                    if existing_template:
                        # Update existing template
                        self._update_existing_template(existing_template, template, db)
                        results["updated_templates"] += 1
                    else:
                        # Add new template
                        db.add(template)
                        results["new_templates"] += 1
                
                logger.info(f"Processed {len(new_templates)} {component_type} templates for {manufacturer}")
                
            except Exception as e:
                logger.error(f"Error syncing {component_type} for {manufacturer}: {e}")
                results["errors"] += 1
        
        # Commit all changes
        try:
            db.commit()
            logger.info(f"Sync completed for {manufacturer}: {results['new_templates']} new, {results['updated_templates']} updated, {results['errors']} errors")
        except Exception as e:
            logger.error(f"Failed to commit templates to database: {e}")
            db.rollback()
            results["errors"] += 1
        
        # Update sync stats
        self.sync_stats["new_templates"] += results["new_templates"]
        self.sync_stats["updated_templates"] += results["updated_templates"]
        self.sync_stats["errors"] += results["errors"]
        self.sync_stats["last_sync"] = datetime.now()
        
        return results
    
    def _update_existing_template(self, existing: DeviceTemplate, new: DeviceTemplate, db: Session):
        """Update an existing template with new data"""
        # Update pricing and availability information
        if hasattr(new, 'unit_price') and new.unit_price:
            existing.unit_price = new.unit_price
        if hasattr(new, 'currency') and new.currency:
            existing.currency = new.currency
        if hasattr(new, 'quantity_available') and new.quantity_available:
            existing.quantity_available = new.quantity_available
        
        # Update description if improved
        if len(new.description) > len(existing.description):
            existing.description = new.description
        
        # Update specifications if they were missing
        if not existing.current_rating and new.current_rating:
            existing.current_rating = new.current_rating
        if not existing.voltage_rating and new.voltage_rating:
            existing.voltage_rating = new.voltage_rating
        if not existing.pole_count and new.pole_count:
            existing.pole_count = new.pole_count
        
        logger.info(f"Updated existing template: {existing.name}")
    
    def sync_all_supported_manufacturers(self, component_types: Optional[List[str]] = None, db: Optional[Session] = None) -> Dict[str, Any]:
        """Sync components for all supported manufacturers"""
        manufacturers = ["Hager", "Schneider Electric", "ABB", "Eaton"]
        
        overall_results = {
            "total_new": 0,
            "total_updated": 0,
            "total_errors": 0,
            "manufacturer_results": {}
        }
        
        for manufacturer in manufacturers:
            try:
                result = self.sync_manufacturer_components(manufacturer, component_types, db)
                overall_results["manufacturer_results"][manufacturer] = result
                
                if "error" not in result:
                    overall_results["total_new"] += result["new_templates"]
                    overall_results["total_updated"] += result["updated_templates"]
                    overall_results["total_errors"] += result["errors"]
                
            except Exception as e:
                logger.error(f"Failed to sync {manufacturer}: {e}")
                overall_results["manufacturer_results"][manufacturer] = {"error": str(e)}
                overall_results["total_errors"] += 1
        
        return overall_results
    
    def get_sync_statistics(self) -> Dict[str, Any]:
        """Get current synchronization statistics"""
        return self.sync_stats.copy()
    
    def validate_api_connection(self) -> bool:
        """Test DigiKey API connection"""
        if not self.digikey_client.is_configured():
            logger.error("DigiKey API credentials not configured")
            return False
        
        if not self.digikey_client.access_token:
            logger.error("DigiKey API not authenticated")
            return False
        
        try:
            # Try a simple search to validate connection
            results = self.digikey_client.search_products("Hager", limit=1)
            return results is not None
        except Exception as e:
            logger.error(f"API connection validation failed: {e}")
            return False


def create_initial_panel_templates(db: Optional[Session] = None) -> int:
    """Create initial panel templates from predefined data"""
    if db is None:
        db = next(get_db())
    
    # Create Hager panel templates
    panel_templates = PanelTemplateMapper.create_hager_panel_templates()
    
    templates_added = 0
    for template in panel_templates:
        existing = db.query(PanelTemplate).filter(
            PanelTemplate.model == template.model,
            PanelTemplate.manufacturer == template.manufacturer
        ).first()
        
        if not existing:
            db.add(template)
            templates_added += 1
        else:
            logger.info(f"Panel template {template.name} already exists")
    
    db.commit()
    logger.info(f"Added {templates_added} new panel templates")
    return templates_added


# Example usage functions
def sync_hager_components(digikey_client: DigiKeyAPIClient) -> Dict[str, Union[int, str, List[str]]]:
    """Convenience function to sync Hager components"""
    sync_service = TemplateSyncService(digikey_client)
    return sync_service.sync_manufacturer_components("Hager")


def demo_digikey_integration() -> Dict[str, Any]:
    """Demo function showing DigiKey integration workflow"""
    # This is a demo function showing how to use the integration
    # In practice, you'd need to authenticate with DigiKey first
    
    results = {
        "status": "demo",
        "message": "DigiKey integration ready",
        "steps_required": [
            "1. Set DIGIKEY_CLIENT_ID and DIGIKEY_CLIENT_SECRET environment variables",
            "2. Get OAuth authorization code from DigiKey",
            "3. Authenticate using client.authenticate_with_code(auth_code)",
            "4. Run sync_service.sync_manufacturer_components('Hager')"
        ],
        "api_configured": False,
        "authentication_url": None
    }
    
    # Try to create client to check configuration
    try:
        client = DigiKeyAPIClient(use_sandbox=True)
        results["api_configured"] = client.is_configured()
        
        if client.is_configured():
            results["authentication_url"] = client.get_oauth_url()
            results["message"] = "API configured, authentication required"
    except Exception as e:
        results["error"] = str(e)
    
    return results