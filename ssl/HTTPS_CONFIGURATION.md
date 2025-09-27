# HTTPS vs HTTP Configuration Guide

## Current Setup (Recommended for Development)

### Default Configuration (HTTP)
- **Frontend**: `http://localhost:3000` 
- **Backend**: `http://localhost:8000`
- **Benefit**: No mixed content issues, simple development setup

### HTTPS Configuration (When Needed)
- **Frontend**: `https://localhost:3000`
- **Backend**: `http://localhost:8000`
- **Use Case**: When DigiKey OAuth requires HTTPS redirect URLs

## How to Switch Between Configurations

### Option 1: Use HTTP for Everything (Default)
```bash
# Start both services normally
npm run dev
# OR use VS Code tasks: "Start Full Application"
```

### Option 2: Use HTTPS Frontend with HTTP Backend
```bash
# In frontend directory
HTTPS=true npm start

# Backend runs on HTTP as normal
cd backend && source venv/bin/activate && uvicorn main:app --reload --port 8000
```

### Option 3: Environment Variable Control
Create/edit `frontend/.env.local`:
```env
HTTPS=false                                    # Use HTTP frontend
REACT_APP_API_BASE_URL=http://localhost:8000/api  # Backend API URL
```

Or for HTTPS frontend:
```env
HTTPS=true                                     # Use HTTPS frontend
REACT_APP_API_BASE_URL=http://localhost:8000/api  # Backend stays HTTP
```

## DigiKey OAuth Considerations

### Development Testing
- For initial development and testing: Use HTTP setup
- DigiKey sandbox may work with HTTP redirect URLs
- Simpler setup without certificate issues

### Production-Like Testing
- If DigiKey requires HTTPS: Use HTTPS frontend + HTTP backend
- Frontend HTTPS satisfies OAuth requirements
- Backend HTTP avoids certificate complexity

### Production Deployment
- Both frontend and backend should use HTTPS
- Use proper SSL certificates from a certificate authority
- Update DigiKey OAuth settings with production URLs

## Troubleshooting

### Mixed Content Errors
- **Problem**: HTTPS frontend calling HTTP backend
- **Solution**: Use HTTP for both services during development

### Certificate Errors
- **Problem**: Self-signed certificates cause browser warnings
- **Solution**: Use HTTP for development, HTTPS only when required

### CORS Issues
- **Problem**: Cross-origin requests blocked
- **Solution**: Backend CORS is configured for both HTTP and HTTPS origins

## VS Code Tasks Available

1. **Start Full Application** - HTTP frontend + HTTP backend (recommended)
2. **Start Frontend Server** - HTTP frontend only
3. **Start Frontend Server (HTTPS)** - HTTPS frontend when needed
4. **Start Backend Server** - HTTP backend (always HTTP for development)