from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import panels, devices, wiring, templates
from database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Electrical Panel Configurator API",
    description="API for configuring electrical panels, devices, and wiring",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(panels.router, prefix="/api/panels", tags=["panels"])
app.include_router(devices.router, prefix="/api/devices", tags=["devices"])
app.include_router(wiring.router, prefix="/api/wiring", tags=["wiring"])
app.include_router(templates.router, prefix="/api/templates", tags=["templates"])

@app.get("/")
def read_root():
    return {"message": "Electrical Panel Configurator API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
