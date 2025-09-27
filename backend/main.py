import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import panels, devices, wiring, templates, template_sync
from database import engine, Base

# Load environment variables from .env file
load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Electrical Panel Configurator API",
    description="API for configuring electrical panels, devices, and wiring",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    """Log configuration on startup"""
    digikey_client_id = os.getenv('DIGIKEY_CLIENT_ID', 'Not set')
    digikey_client_secret = os.getenv('DIGIKEY_CLIENT_SECRET', 'Not set')
    sandbox_mode = os.getenv('DIGIKEY_SANDBOX', 'true')
    
    print("🔌 Electrical Panel Configurator API Starting...")
    print(f"   DigiKey Client ID: {'✅ Set' if digikey_client_id != 'Not set' else '❌ Not set'}")
    print(f"   DigiKey Client Secret: {'✅ Set' if digikey_client_secret != 'Not set' else '❌ Not set'}")
    print(f"   Sandbox Mode: {sandbox_mode}")
    print("   API Documentation: http://127.0.0.1:8000/docs")
    print("🚀 Ready to accept requests!")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://localhost:3000",  # Frontend HTTPS (for DigiKey OAuth if needed)
        "http://localhost:3000",   # Frontend HTTP (for development)
        "http://127.0.0.1:3000",   # Alternative frontend HTTP
        "https://127.0.0.1:3000"   # Alternative frontend HTTPS
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(panels.router, prefix="/api/panels", tags=["panels"])
app.include_router(devices.router, prefix="/api/devices", tags=["devices"])
app.include_router(wiring.router, prefix="/api/wiring", tags=["wiring"])
app.include_router(templates.router, prefix="/api/templates", tags=["templates"])
app.include_router(template_sync.router, tags=["template-sync"])

@app.get("/")
def read_root():
    return {"message": "Electrical Panel Configurator API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
