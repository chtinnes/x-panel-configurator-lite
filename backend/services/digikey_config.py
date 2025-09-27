"""
DigiKey API Configuration
Configuration settings for DigiKey API integration
"""

# DigiKey API Endpoints
DIGIKEY_BASE_URL = "https://api.digikey.com"
DIGIKEY_SANDBOX_URL = "https://sandbox-api.digikey.com"  # Free sandbox for development
DIGIKEY_AUTH_URL = "https://api.digikey.com"  # OAuth 2.0 authorization endpoint

# API Version
API_VERSION = "v3"
PRODUCT_INFO_VERSION = "v4"

# OAuth 2.0 Configuration
# These would be set via environment variables in production
CLIENT_ID = None  # Set via DIGIKEY_CLIENT_ID env var
CLIENT_SECRET = None  # Set via DIGIKEY_CLIENT_SECRET env var
REDIRECT_URI = "https://localhost:3000/callback"  # Your app's callback URL

# Rate Limiting (Free Sandbox Limits)
RATE_LIMIT_PER_MINUTE = 120
RATE_LIMIT_PER_DAY = 10000  # Typical free tier daily limit

# Request Headers
DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "ElectricalPanelConfigurator/1.0"
}

# Electrical Component Categories
ELECTRICAL_CATEGORIES = {
    "circuit_breakers": {
        "search_terms": ["circuit breaker", "MCB", "miniature circuit breaker"],
        "manufacturers": ["Hager", "Schneider Electric", "ABB", "Eaton", "Siemens"]
    },
    "rcd_devices": {
        "search_terms": ["RCD", "residual current device", "earth leakage"],
        "manufacturers": ["Hager", "Schneider Electric", "ABB", "Eaton"]
    },
    "rcbo_devices": {
        "search_terms": ["RCBO", "residual current circuit breaker"],
        "manufacturers": ["Hager", "Schneider Electric", "ABB", "Eaton"]
    },
    "smart_meters": {
        "search_terms": ["smart meter", "digital meter", "energy meter"],
        "manufacturers": ["Hager", "Schneider Electric", "ABB", "Siemens"]
    },
    "contactors": {
        "search_terms": ["contactor", "motor starter"],
        "manufacturers": ["Schneider Electric", "ABB", "Siemens", "Eaton"]
    }
}

# Device Type Mapping
DEVICE_TYPE_MAPPING = {
    "Circuit Breakers": "MCB",
    "Miniature Circuit Breaker": "MCB", 
    "Residual Current Device": "RCD",
    "RCD": "RCD",
    "RCBO": "RCBO",
    "Residual Current Circuit Breaker": "RCBO",
    "Smart Meter": "SMART_METER",
    "Energy Meter": "SMART_METER",
    "Contactor": "CONTACTOR"
}

# Specification Extraction Patterns
CURRENT_RATING_PATTERNS = [
    r"(\d+)A",  # "16A", "32A"
    r"(\d+)\s*Amp",  # "16 Amp"
    r"Current.*?(\d+)A",  # "Current Rating: 16A"
]

VOLTAGE_RATING_PATTERNS = [
    r"(\d+)V",  # "230V", "400V"
    r"(\d+)\s*Volt",  # "230 Volt"
    r"Voltage.*?(\d+)V",  # "Voltage: 230V"
]

POLE_COUNT_PATTERNS = [
    r"(\d+)\s*Pole",  # "2 Pole", "4 Pole"
    r"(\d+)P",  # "2P", "4P"
    r"(\d+)\s*Way",  # "2 Way"
]