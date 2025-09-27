"""
Template Sync API Router
Endpoints for managing template synchronization with DigiKey API
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Dict, List, Optional, Any
import logging
import os

from database import get_db
from services.digikey_client import DigiKeyAPIClient
from services.template_sync import TemplateSyncService, demo_digikey_integration, create_initial_panel_templates
from pydantic import BaseModel

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/template-sync", tags=["template-sync"])

# Global DigiKey client (will be initialized when needed)
_digikey_client: Optional[DigiKeyAPIClient] = None

def get_digikey_client() -> DigiKeyAPIClient:
    """Get or create DigiKey API client"""
    global _digikey_client
    if _digikey_client is None:
        _digikey_client = DigiKeyAPIClient(use_sandbox=True)
    return _digikey_client

# Request/Response Models
class SyncRequest(BaseModel):
    manufacturers: Optional[List[str]] = ["Hager"]
    component_types: Optional[List[str]] = ["circuit_breakers", "rcd_devices", "rcbo_devices"]
    
class AuthRequest(BaseModel):
    authorization_code: str

class SyncResponse(BaseModel):
    status: str
    message: str
    results: Optional[Dict[str, Any]] = None

@router.get("/status")
async def get_sync_status() -> Dict[str, Any]:
    """Get current synchronization status and configuration"""
    client = get_digikey_client()
    
    status = {
        "api_configured": client.is_configured(),
        "authenticated": bool(client.access_token),
        "sandbox_mode": client.use_sandbox,
        "sync_service_ready": False,
        "sync_stats": {}
    }
    
    if status["api_configured"] and status["authenticated"]:
        sync_service = TemplateSyncService(client)
        status["sync_service_ready"] = True
        status["sync_stats"] = sync_service.get_sync_statistics()
    
    return status

@router.get("/demo")
async def demo_integration() -> Dict[str, Any]:
    """Demo endpoint showing DigiKey integration setup"""
    return demo_digikey_integration()

@router.get("/auth-url")
async def get_auth_url() -> Dict[str, str]:
    """Get DigiKey OAuth authorization URL"""
    client = get_digikey_client()
    
    if not client.is_configured():
        raise HTTPException(
            status_code=400, 
            detail="DigiKey API not configured. Set DIGIKEY_CLIENT_ID and DIGIKEY_CLIENT_SECRET environment variables."
        )
    
    try:
        auth_url = client.get_oauth_url()
        return {
            "authorization_url": auth_url,
            "instructions": "Visit this URL to authorize the application, then use the authorization code with the /authenticate endpoint"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate auth URL: {e}")

@router.get("/callback")
async def oauth_callback(code: Optional[str] = None, error: Optional[str] = None):
    """Handle DigiKey OAuth callback and redirect back to frontend"""
    from fastapi.responses import RedirectResponse
    
    base_url = "https://localhost:3000"  # Frontend URL (HTTPS for OAuth)
    
    if error:
        # Redirect to frontend with error
        return RedirectResponse(url=f"{base_url}/?error={error}")
    
    if not code:
        # Redirect to frontend with error
        return RedirectResponse(url=f"{base_url}/?error=no_code")
    
    # Redirect to frontend with the authorization code
    return RedirectResponse(url=f"{base_url}/?code={code}")

@router.get("/callback-info")
async def callback_info(code: Optional[str] = None, error: Optional[str] = None) -> Dict[str, Any]:
    """Alternative callback endpoint that returns JSON (for API testing)"""
    if error:
        raise HTTPException(
            status_code=400,
            detail=f"OAuth authorization failed: {error}"
        )
    
    if not code:
        raise HTTPException(
            status_code=400,
            detail="No authorization code received from DigiKey"
        )
    
    # Return the code for the frontend to handle
    return {
        "authorization_code": code,
        "status": "success",
        "message": "Authorization code received successfully"
    }

@router.post("/authenticate")
async def authenticate(auth_request: AuthRequest) -> SyncResponse:
    """Authenticate with DigiKey API using authorization code"""
    client = get_digikey_client()
    
    if not client.is_configured():
        raise HTTPException(
            status_code=400,
            detail="DigiKey API not configured. Set DIGIKEY_CLIENT_ID and DIGIKEY_CLIENT_SECRET environment variables."
        )
    
    success = client.authenticate_with_code(auth_request.authorization_code)
    
    if success:
        return SyncResponse(
            status="success",
            message="Successfully authenticated with DigiKey API",
            results={"authenticated": True, "access_token_available": True}
        )
    else:
        raise HTTPException(
            status_code=400,
            detail="Failed to authenticate with DigiKey API. Please check your authorization code."
        )

@router.post("/sync")
async def sync_templates(
    sync_request: SyncRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
) -> SyncResponse:
    """Synchronize device templates from DigiKey API"""
    client = get_digikey_client()
    
    if not client.is_configured():
        raise HTTPException(
            status_code=400,
            detail="DigiKey API not configured. Set DIGIKEY_CLIENT_ID and DIGIKEY_CLIENT_SECRET environment variables."
        )
    
    if not client.access_token:
        raise HTTPException(
            status_code=401,
            detail="DigiKey API not authenticated. Please authenticate first using /authenticate endpoint."
        )
    
    # Validate API connection
    sync_service = TemplateSyncService(client)
    if not sync_service.validate_api_connection():
        raise HTTPException(
            status_code=503,
            detail="Cannot connect to DigiKey API. Please check your authentication."
        )
    
    # Start synchronization
    try:
        results = {}
        manufacturers = sync_request.manufacturers or ["Hager"]
        
        for manufacturer in manufacturers:
            logger.info(f"Starting sync for manufacturer: {manufacturer}")
            result = sync_service.sync_manufacturer_components(
                manufacturer=manufacturer,
                component_types=sync_request.component_types,
                db=db
            )
            results[manufacturer] = result
        
        return SyncResponse(
            status="success",
            message=f"Synchronized templates for {len(manufacturers)} manufacturers",
            results=results
        )
        
    except Exception as e:
        logger.error(f"Template sync failed: {e}")
        raise HTTPException(status_code=500, detail=f"Synchronization failed: {e}")

@router.post("/sync/{manufacturer}")
async def sync_manufacturer_templates(
    manufacturer: str,
    component_types: Optional[List[str]] = None,
    db: Session = Depends(get_db)
) -> SyncResponse:
    """Synchronize templates for a specific manufacturer"""
    client = get_digikey_client()
    
    if not client.is_configured() or not client.access_token:
        raise HTTPException(
            status_code=401,
            detail="DigiKey API not configured or authenticated"
        )
    
    sync_service = TemplateSyncService(client)
    
    try:
        if component_types is None:
            component_types = ["circuit_breakers", "rcd_devices", "rcbo_devices"]
        
        result = sync_service.sync_manufacturer_components(
            manufacturer=manufacturer,
            component_types=component_types,
            db=db
        )
        
        return SyncResponse(
            status="success",
            message=f"Synchronized {manufacturer} templates",
            results={manufacturer: result}
        )
        
    except Exception as e:
        logger.error(f"Failed to sync {manufacturer}: {e}")
        raise HTTPException(status_code=500, detail=f"Sync failed: {e}")

@router.get("/stats")
async def get_sync_stats() -> Dict[str, Any]:
    """Get synchronization statistics"""
    client = get_digikey_client()
    
    if not client.access_token:
        return {"error": "Not authenticated"}
    
    sync_service = TemplateSyncService(client)
    return sync_service.get_sync_statistics()

@router.post("/init-panels")
async def initialize_panel_templates(db: Session = Depends(get_db)) -> SyncResponse:
    """Initialize default panel templates"""
    try:
        templates_added = create_initial_panel_templates(db)
        return SyncResponse(
            status="success",
            message=f"Initialized {templates_added} panel templates",
            results={"panel_templates_added": templates_added}
        )
    except Exception as e:
        logger.error(f"Failed to initialize panel templates: {e}")
        raise HTTPException(status_code=500, detail=f"Initialization failed: {e}")

@router.get("/supported-manufacturers")
async def get_supported_manufacturers() -> Dict[str, Any]:
    """Get list of supported manufacturers and component types"""
    return {
        "manufacturers": ["Hager", "Schneider Electric", "ABB", "Eaton"],
        "component_types": ["circuit_breakers", "rcd_devices", "rcbo_devices", "smart_meters", "contactors"],
        "note": "Templates are created from DigiKey API product data"
    }