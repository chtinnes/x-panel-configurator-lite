# DigiKey OAuth Configuration

## Frontend OAuth Callback Route

The frontend now has a dedicated OAuth callback route that handles the DigiKey OAuth flow:

### Route Configuration
- **Frontend Route**: `/template-sync/callback`
- **Full URL**: `https://localhost:3000/template-sync/callback`

### DigiKey API Configuration

**Use this URL as your DigiKey OAuth Redirect URI:**

```
https://localhost:3000/template-sync/callback
```

### OAuth Flow

1. **Authorization Request**: User clicks OAuth button in frontend
2. **DigiKey Redirect**: DigiKey redirects to `https://localhost:3000/template-sync/callback?code=...`
3. **Frontend Processing**: React app captures the authorization code
4. **Backend Authentication**: Frontend sends code to backend via API call to:
   ```
   POST https://localhost:8001/api/template-sync/authenticate
   ```
5. **Token Exchange**: Backend exchanges code for access token with DigiKey
6. **Success Redirect**: Frontend redirects user to admin panel

### API Endpoints

- **Get OAuth URL**: `GET https://localhost:8001/api/template-sync/auth-url`
- **Authenticate**: `POST https://localhost:8001/api/template-sync/authenticate`
- **Status Check**: `GET https://localhost:8001/api/template-sync/status`

### Development URLs

- **Frontend**: `https://localhost:3000`
- **Backend API**: `https://localhost:8001/api`
- **API Documentation**: `https://localhost:8001/docs`

### File Changes Made

1. **Frontend**:
   - Added React Router dependency
   - Created `DigiKeyOAuthCallback` component
   - Updated `App.tsx` with routing
   - Added SSL certificate helper

2. **Backend**:
   - Updated DigiKey client redirect URIs to use frontend callback
   - Fixed CORS configuration for HTTPS frontend
   - Maintained existing API endpoints

### Testing

1. Start both servers: `Start Full Application (HTTPS)` task in VS Code
2. Navigate to: `https://localhost:3000`
3. Accept SSL certificates for both frontend and backend
4. Go to DigiKey Admin section
5. Click "Get Authorization URL"
6. Follow OAuth flow

The OAuth callback URL that DigiKey will redirect to is:
**`https://localhost:3000/template-sync/callback`**