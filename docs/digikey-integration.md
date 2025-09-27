# DigiKey API Integration Guide

## 🎯 Overview

This integration allows your electrical panel configurator to automatically populate device templates from DigiKey's comprehensive electrical component database. Instead of manually entering component specifications, you can now sync real product data from major manufacturers like Hager, Schneider Electric, ABB, and Eaton.

## 🚀 Benefits

- ✅ **Real manufacturer data** - No more manual data entry
- ✅ **Current pricing & availability** - Live market information
- ✅ **Automated updates** - Keep templates fresh via API
- ✅ **Professional specifications** - Trusted distributor data
- ✅ **Free sandbox access** - Test without costs

## 📋 Prerequisites

### 1. DigiKey Developer Account

1. Visit [https://developer.digikey.com/](https://developer.digikey.com/)
2. Click "Register / Login"
3. Create account using your DigiKey customer credentials
4. If you don't have a DigiKey account, register at [https://www.digikey.com/](https://www.digikey.com/)

### 2. Create API Application

1. Login to DigiKey Developer Portal
2. Navigate to "My Apps"
3. Click "Create New App"
4. Fill in application details:
   - **App Name**: "Electrical Panel Configurator"
   - **Description**: "Template synchronization for electrical components"
   - **Redirect URI**: `https://localhost:3000/callback`
   - **Environment**: Select "Sandbox" for development

### 3. Get API Credentials

After creating your app, you'll receive:
- **Client ID** - Public identifier for your app
- **Client Secret** - Private key (keep secure!)

## ⚙️ Configuration

### 1. Set Environment Variables

Create a `.env` file in your backend directory:

```bash
# DigiKey API Credentials
DIGIKEY_CLIENT_ID=your_client_id_here
DIGIKEY_CLIENT_SECRET=your_client_secret_here

# Optional: Force sandbox mode (default: true for development)
DIGIKEY_USE_SANDBOX=true
```

### 2. Install Dependencies

```bash
cd backend
pip install requests urllib3
```

### 3. Start the Backend

```bash
cd backend
source venv/bin/activate  # If using virtual environment
uvicorn main:app --reload --port 8000
```

## 🔐 Authentication Flow

DigiKey uses OAuth 2.0 for secure API access. Here's the authentication process:

### Step 1: Get Authorization URL

```bash
curl http://localhost:8000/api/template-sync/auth-url
```

Response:
```json
{
  "authorization_url": "https://sso.digikey.com/authorization?...",
  "instructions": "Visit this URL to authorize the application..."
}
```

### Step 2: Authorize Application

1. Visit the authorization URL in your browser
2. Login with your DigiKey credentials
3. Authorize your application
4. Copy the authorization code from the callback URL

### Step 3: Exchange Code for Token

```bash
curl -X POST http://localhost:8000/api/template-sync/authenticate \
  -H "Content-Type: application/json" \
  -d '{"authorization_code": "your_auth_code_here"}'
```

## 🔄 Template Synchronization

### Check API Status

```bash
curl http://localhost:8000/api/template-sync/status
```

### Sync Hager Components

```bash
curl -X POST http://localhost:8000/api/template-sync/sync/Hager \
  -H "Content-Type: application/json"
```

### Sync Multiple Manufacturers

```bash
curl -X POST http://localhost:8000/api/template-sync/sync \
  -H "Content-Type: application/json" \
  -d '{
    "manufacturers": ["Hager", "Schneider Electric", "ABB"],
    "component_types": ["circuit_breakers", "rcd_devices", "rcbo_devices"]
  }'
```

### Initialize Panel Templates

```bash
curl -X POST http://localhost:8000/api/template-sync/init-panels
```

## 🏗️ Architecture

### Component Structure

```
backend/
├── services/
│   ├── __init__.py
│   ├── digikey_config.py      # API configuration & constants
│   ├── digikey_client.py      # API client with OAuth & rate limiting
│   ├── template_mapper.py     # Maps DigiKey data to templates
│   └── template_sync.py       # Orchestrates synchronization
├── routers/
│   └── template_sync.py       # API endpoints for sync operations
└── models.py                  # Database models (updated)
```

### Data Flow

1. **API Client** searches DigiKey for electrical components
2. **Specification Extraction** parses technical parameters
3. **Template Mapping** converts to DeviceTemplate format
4. **Database Sync** updates templates with conflict resolution
5. **Rate Limiting** ensures API usage stays within limits

### Supported Component Types

| Component Type | Description | Slot Usage |
|----------------|-------------|------------|
| `circuit_breakers` | MCBs, miniature circuit breakers | 1-4 slots |
| `rcd_devices` | Residual current devices | 2-4 slots |
| `rcbo_devices` | Combined MCB + RCD | 2 slots |
| `smart_meters` | Digital energy meters | 4 slots |
| `contactors` | Motor starters, contactors | 3 slots |

## 📊 API Endpoints

### Authentication

- `GET /api/template-sync/auth-url` - Get OAuth authorization URL
- `POST /api/template-sync/authenticate` - Exchange auth code for token

### Synchronization

- `GET /api/template-sync/status` - Check API status and configuration
- `POST /api/template-sync/sync` - Sync templates for multiple manufacturers
- `POST /api/template-sync/sync/{manufacturer}` - Sync specific manufacturer
- `POST /api/template-sync/init-panels` - Initialize panel templates

### Information

- `GET /api/template-sync/stats` - Get sync statistics
- `GET /api/template-sync/supported-manufacturers` - List supported manufacturers
- `GET /api/template-sync/demo` - Demo integration status

## 🔧 Rate Limiting

DigiKey API has rate limits to ensure fair usage:

- **Sandbox**: ~120 requests/minute, ~10,000 requests/day
- **Production**: Higher limits available with paid plans

The integration includes automatic rate limiting and retry logic.

## 🛠️ Troubleshooting

### "API not configured"
- Check environment variables are set correctly
- Ensure `.env` file is in the correct location
- Restart the backend server after adding variables

### "Authentication failed"
- Verify Client ID and Client Secret are correct
- Check authorization code hasn't expired (short lifespan)
- Ensure redirect URI matches exactly

### "No products found"
- Try different search terms
- Check manufacturer name spelling
- Some manufacturers may have limited DigiKey inventory

### Rate Limits Exceeded
- Wait for rate limit window to reset
- Reduce sync frequency
- Consider upgrading to DigiKey production API

## 📈 Example Integration Workflow

```python
# In your application code
from backend.services.digikey_client import DigiKeyAPIClient
from backend.services.template_sync import TemplateSyncService

# Initialize client
client = DigiKeyAPIClient(use_sandbox=True)

# Authenticate (after getting auth code)
client.authenticate_with_code("your_auth_code")

# Sync templates
sync_service = TemplateSyncService(client)
result = sync_service.sync_manufacturer_components("Hager")

print(f"Added {result['new_templates']} new templates")
```

## 🎯 Next Steps

1. **Set up DigiKey account** and get API credentials
2. **Configure environment** variables
3. **Test authentication** flow
4. **Run first sync** with Hager components
5. **Schedule periodic syncs** for fresh data

## 💡 Pro Tips

- Use sandbox environment for development
- Start with one manufacturer to test
- Monitor rate limits during bulk syncs  
- Keep API credentials secure and private
- Schedule syncs during low-traffic periods

This integration transforms your manual template management into an automated, data-driven system that stays current with real market information!