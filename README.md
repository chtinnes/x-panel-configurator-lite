# Electrical Panel Configurator

A full-stack web application for configuring electrical panels, specifically designed for Hager Volta electrical panel series. This tool helps electricians and engineers design electrical installations by providing an intuitive drag-and-drop interface for placing devices and configuring wiring connections.

![Project Status](https://img.shields.io/badge/Status-Functional-## 📖 Documentation

Comprehensive documentation is available in the `/docs` folder and `/ssl` folder:

### Core Documentation
- **[Overview](./docs/README.md)**: Project overview and quick start guide
- **[Requirements](./docs/requirements.md)**: Detailed functional and technical requirements
- **[Features](./docs/features.md)**: Complete feature documentation with user workflows
- **[Architecture](./docs/architecture.md)**: Software architecture with domain models and diagrams
- **[API Reference](./docs/api.md)**: Complete API documentation with examples
- **[Developer Guide](./docs/developer-guide.md)**: Development setup, standards, and contribution guidelines

### HTTPS & DigiKey Integration
- **[SSL Setup Guide](ssl/README.md)**: HTTPS development environment setup
- **[Certificate Generation](ssl/generate-certificates.sh)**: Automated SSL certificate creation
- **[DigiKey OAuth Setup](ssl/DIGIKEY_OAUTH_SETUP.md)**: Complete OAuth integration guide  
- **[HTTPS Configuration](ssl/HTTPS_CONFIGURATION.md)**: Detailed HTTPS configuration instructions

### API Documentation
- **Interactive API Docs**: 
  - HTTP: http://localhost:8000/docs
  - HTTPS: https://localhost:8001/docs
- **Alternative API Docs**: 
  - HTTP: http://localhost:8000/redoc
  - HTTPS: https://localhost:8001/redocn)
![Backend](https://img.shields.io/badge/Backend-FastAPI-009688)
![Frontend](https://img.shields.io/badge/Frontend-React+TypeScript-61DAFB)
![Database](https://img.shields.io/badge/Database-SQLite-003B57)

## ✨ Features

### ✅ Core Features (Implemented)
- **Panel Management**: Create, view, update, and delete electrical panels
- **Device Library**: Comprehensive library of Hager electrical devices (MCBs, RCDs, RCBOs, Smart Meters)
- **Drag & Drop Interface**: Intuitive drag-and-drop device placement
- **Panel Templates**: Pre-configured Hager Volta panel templates (12-way, 18-way, 24-way)
- **Device Configuration**: Configure device settings like current ratings and labels
- **RESTful API**: Complete REST API with OpenAPI/Swagger documentation
- **Modern UI**: Material-UI components with responsive design

### 🔧 Additional Features (Ready for Extension)
- **Wiring Management**: Framework for managing wire connections between devices
- **Standards Compliance**: UK/EU electrical standards integration
- **Real-time Updates**: Live panel configuration updates

## 🚀 Quick Start

### Prerequisites
- **Python 3.9+** (Backend)
- **Node.js 16+** (Frontend)  
- **npm or yarn** (Package manager)
- **OpenSSL** (For HTTPS development - required for DigiKey OAuth)

### Development Setup Options

#### Option 1: HTTP Development (Simple)
For basic development without DigiKey integration:

1. **Backend Setup**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn main:app --reload --port 8000
   ```

2. **Frontend Setup**:
   ```bash
   cd frontend
   npm install
   npm start
   ```

3. **Access**: http://localhost:3000

#### Option 2: HTTPS Development (Required for DigiKey)
For full functionality including DigiKey OAuth integration:

1. **Generate SSL Certificates**:
   ```bash
   cd ssl
   ./generate-certificates.sh
   ```

2. **Use VS Code Tasks**:
   - **Ctrl/Cmd + Shift + P** → "Tasks: Run Task"
   - Select **"Start Full Application (HTTPS)"**

3. **Access**: https://localhost:3000 (accept certificate warnings)

⚠️ **Important**: DigiKey OAuth integration requires HTTPS. The OAuth callback URL must use HTTPS protocol.

### Configuration Switching
Use the provided script to easily switch between HTTP and HTTPS:

```bash
# Switch to HTTPS (required for DigiKey OAuth)
./switch-config.sh https

# Switch to HTTP (for basic development)
./switch-config.sh http
```

## ✨ New Features

### 🔌 DigiKey API Integration
Automated component template synchronization with real manufacturer data:

- **OAuth 2.0 Authentication**: Secure integration with DigiKey's API
- **HTTPS Required**: DigiKey OAuth callbacks require HTTPS protocol
- **Real-time component data** from DigiKey's electrical component catalog
- **Automated template creation** for MCBs, RCDs, RCBOs, and smart meters
- **Live pricing & availability** information
- **Support for major manufacturers**: Hager, Schneider Electric, ABB, Eaton
- **Free sandbox access** for development and testing

**Setup Requirements:**
1. **HTTPS Development Environment**: Required for OAuth callbacks
2. **DigiKey Developer Account**: Get API credentials from [developer.digikey.com](https://developer.digikey.com/)
3. **OAuth Callback URL**: Configure `https://localhost:3000/template-sync/callback` in DigiKey app settings

**Quick Start:**
```bash
# 1. Generate SSL certificates
cd ssl && ./generate-certificates.sh

# 2. Set DigiKey API credentials
export DIGIKEY_CLIENT_ID="your_client_id"
export DIGIKEY_CLIENT_SECRET="your_client_secret"

# 3. Start HTTPS servers
# Use VS Code task: "Start Full Application (HTTPS)"

# 4. Connect to DigiKey via admin interface
# Navigate to https://localhost:3000 → DigiKey Admin → Connect to DigiKey
```

**Documentation:**
- **[SSL Setup Guide](ssl/README.md)**: HTTPS development configuration
- **[DigiKey OAuth Setup](ssl/DIGIKEY_OAUTH_SETUP.md)**: Complete OAuth integration guide
- **[HTTPS Configuration](ssl/HTTPS_CONFIGURATION.md)**: Detailed HTTPS setup instructions

## 🏗️ Architecture

### Backend
- **FastAPI**: Modern Python web framework with automatic OpenAPI documentation
- **SQLAlchemy**: Object-Relational Mapping (ORM) for database operations
- **SQLite**: Lightweight database for development
- **Pydantic**: Data validation and serialization using Python type annotations
- **Uvicorn**: Lightning-fast ASGI server

### Frontend
- **React 18**: Modern React with hooks and TypeScript
- **TypeScript**: Type-safe JavaScript for better development experience
- **Material-UI v7**: Google's Material Design components
- **React DnD**: Smooth drag-and-drop functionality
- **Axios**: Promise-based HTTP client for API communication

## 📁 Project Structure

```
electrical-panel-configurator/
├── backend/                    # Python FastAPI backend
│   ├── main.py                 # Application entry point
│   ├── database.py             # Database configuration
│   ├── models.py               # SQLAlchemy models
│   ├── schemas.py              # Pydantic schemas
│   ├── requirements.txt        # Python dependencies
│   ├── panel_configurator.db   # SQLite database
│   ├── services/               # Business logic services
│   │   ├── digikey_client.py   # DigiKey API integration
│   │   └── template_sync.py    # Template synchronization
│   └── routers/                # API route handlers
│       ├── panels.py           # Panel management
│       ├── devices.py          # Device library
│       ├── wiring.py           # Wiring configuration
│       └── template_sync.py    # DigiKey API endpoints
├── frontend/                   # React TypeScript frontend
│   ├── public/
│   ├── src/
│   │   ├── App.tsx             # Main application with routing
│   │   ├── components/         # React components
│   │   │   ├── PanelSelector.tsx
│   │   │   ├── PanelView.tsx
│   │   │   ├── DeviceLibrary.tsx
│   │   │   ├── WiringView.tsx
│   │   │   ├── DigiKeyAdmin.tsx         # DigiKey administration
│   │   │   ├── DigiKeyOAuthCallback.tsx # OAuth callback handler
│   │   │   └── SSLCertificateHelper.tsx # HTTPS helper
│   │   ├── services/
│   │   │   └── api.ts          # API service layer
│   │   └── types/
│   │       └── index.ts        # TypeScript definitions
│   ├── package.json
│   └── tsconfig.json
├── ssl/                        # SSL certificates and HTTPS configuration
│   ├── README.md               # SSL setup documentation
│   ├── generate-certificates.sh # Automated certificate generation
│   ├── localhost.conf          # OpenSSL configuration
│   ├── DIGIKEY_OAUTH_SETUP.md  # DigiKey OAuth guide
│   └── HTTPS_CONFIGURATION.md  # HTTPS setup instructions
├── .vscode/                    # VS Code configuration
│   └── tasks.json              # Development tasks (HTTP/HTTPS)
├── switch-config.sh            # HTTP/HTTPS configuration switcher
└── README.md                   # This file
```

## 🎯 Usage Guide

### Creating Your First Panel

1. **From Template** (Recommended):
   - Click on "Panel Selection" in the sidebar
   - Choose from Hager Volta templates:
     - **12-way (VD112)**: 63A, suitable for small homes
     - **18-way (VD118)**: 100A, suitable for medium homes
     - **24-way (VD124)**: 100A, suitable for large homes

2. **Custom Panel**:
   - Fill in panel specifications manually
   - Specify number of slots, voltage, and current rating

### Configuring Devices

1. **Drag & Drop**:
   - Browse the device library in the sidebar
   - Drag devices to empty panel slots
   - Visual feedback shows valid drop zones

2. **Device Configuration**:
   - Click on placed devices to configure settings
   - Set current ratings, labels, and descriptions
   - Remove devices with the "Remove" button

3. **Device Types**:
   - **MCBs**: Single-slot circuit breakers (6A-63A)
   - **RCDs**: Residual current devices for earth leakage protection
   - **RCBOs**: Combined MCB+RCD (requires 2 slots)
   - **Smart Meters**: Digital meters (requires 4 slots)

### Wiring Configuration

1. Switch to "Wiring Configuration" view
2. Add wire connections between devices
3. Configure wire properties (color, cross-section, length)
4. Follow UK/EU electrical standards

## 🔌 API Documentation

### Panel Endpoints
```
GET    /api/panels/                     # List all panels
POST   /api/panels/                     # Create new panel
GET    /api/panels/{id}                 # Get specific panel
PUT    /api/panels/{id}                 # Update panel
DELETE /api/panels/{id}                 # Delete panel
GET    /api/panels/templates/hager-volta # Get templates
```

### Device Endpoints
```
GET    /api/devices/types               # List device types
POST   /api/devices/types               # Create device type
GET    /api/devices/library/hager       # Get Hager device library
```

### Wiring Endpoints
```
GET    /api/wiring/panel/{panel_id}     # Get panel wiring
POST   /api/wiring/                     # Create wire connection
PUT    /api/wiring/{wire_id}            # Update wire
DELETE /api/wiring/{wire_id}            # Delete wire
GET    /api/wiring/standards/colors     # Get wire color standards
GET    /api/wiring/standards/cross-sections # Get cross-section standards
```

## 🔧 Development

### Database Schema

#### Core Models
- **Panel**: Electrical panel configuration
- **DeviceType**: Available electrical devices
- **PanelSlot**: Individual panel positions with device assignments
- **Wire**: Electrical connections between devices

#### Key Relationships
- One panel has many slots
- One device type can be assigned to many slots
- Wires connect between slots or external points

### Running Tests
```bash
# Backend tests (when implemented)
cd backend && python -m pytest

# Frontend tests
cd frontend && npm test
```

### Building for Production
```bash
# Backend
cd backend
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker

# Frontend
cd frontend
npm run build
```

### VS Code Integration
Use the predefined tasks in `.vscode/tasks.json`:

#### HTTP Development (Basic)
1. **Ctrl/Cmd + Shift + P** → "Tasks: Run Task"
2. Select **"Start Full Application"** (HTTP mode)

#### HTTPS Development (DigiKey OAuth)
1. **Ctrl/Cmd + Shift + P** → "Tasks: Run Task"  
2. Select **"Start Full Application (HTTPS)"**
3. Accept SSL certificate warnings in browser

#### Individual Services
- **"Start Backend Server"** - HTTP backend only
- **"Start Backend Server (HTTPS)"** - HTTPS backend only  
- **"Start Frontend Server"** - HTTP frontend only
- **"Start Frontend Server (HTTPS)"** - HTTPS frontend only

💡 **Tip**: Use HTTPS tasks when working with DigiKey integration, HTTP tasks for basic development.

## ⚡ Electrical Standards

The application follows UK/EU electrical regulations:

### Wire Standards
- **Colors**: Brown (Live), Blue (Neutral), Green/Yellow (Earth)
- **Cross-Sections**: 1.0mm², 1.5mm², 2.5mm², 4.0mm², 6.0mm², 10.0mm²
- **Current Ratings**: 6A, 10A, 16A, 20A, 25A, 32A, 40A, 50A, 63A

### Safety Requirements
- **RCD Protection**: 30mA for socket circuits
- **Proper Current Ratings**: Wire cross-sections match device ratings
- **Load Balancing**: Distribution across phases
- **Earthing**: Proper earth bonding requirements

## 🛠️ Troubleshooting

### Common Issues

1. **DigiKey OAuth not working**:
   - Ensure HTTPS is enabled: `./switch-config.sh https`
   - Verify SSL certificates: `cd ssl && ./generate-certificates.sh`  
   - Check DigiKey callback URL: `https://localhost:3000/template-sync/callback`
   - Accept certificate warnings in browser for both frontend and backend

2. **SSL Certificate warnings**:
   - Navigate to https://localhost:3000 and https://localhost:8001
   - Click "Advanced" → "Proceed to localhost (unsafe)" for both URLs
   - Or regenerate certificates: `cd ssl && ./generate-certificates.sh`

3. **Frontend won't start**:
   ```bash
   cd frontend
   rm -rf node_modules package-lock.json
   npm install
   npm start
   ```

4. **Backend API errors**:
   ```bash
   cd backend
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **Database issues**:
   ```bash
   cd backend
   rm panel_configurator.db  # Reset database
   # Restart backend to recreate with sample data
   ```

6. **CORS issues**:
   - Ensure backend runs on correct port (8000 for HTTP, 8001 for HTTPS)
   - Ensure frontend runs on port 3000

## 🚀 Future Enhancements

- [ ] **Advanced Wiring**: Circuit diagram generation
- [ ] **Load Calculations**: Automatic load balancing
- [ ] **Export Features**: PDF reports, CAD formats
- [ ] **Multi-Phase Support**: Three-phase panel configurations
- [ ] **User Management**: Authentication and project sharing
- [ ] **Mobile App**: Field configuration tool
- [ ] **AI Assistant**: Intelligent device recommendations
- [ ] **Compliance Checking**: Automatic regulation validation

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines
- Follow electrical industry terminology accurately
- Ensure all current ratings and specifications are realistic
- Validate that wire cross-sections match current ratings
- Use proper electrical symbols and colors in the UI
- Maintain data consistency between frontend and backend

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Hager Group**: For electrical component specifications and standards
- **UK Electrical Regulations**: 17th/18th Edition wiring regulations
- **FastAPI Community**: For excellent documentation and examples
- **Material-UI Team**: For beautiful and accessible React components
- **React DnD**: For smooth drag-and-drop functionality

## � Documentation

Comprehensive documentation is available in the `/docs` folder:

- **[Overview](./docs/README.md)**: Project overview and quick start guide
- **[Requirements](./docs/requirements.md)**: Detailed functional and technical requirements
- **[Features](./docs/features.md)**: Complete feature documentation with user workflows
- **[Architecture](./docs/architecture.md)**: Software architecture with domain models and diagrams
- **[API Reference](./docs/api.md)**: Complete API documentation with examples
- **[Developer Guide](./docs/developer-guide.md)**: Development setup, standards, and contribution guidelines

## �📞 Support

For support and questions:
- **Create an issue** in the GitHub repository
- **Check the documentation** in the `/docs` folder
- **Review the API docs** at http://localhost:8000/docs
- **Check Copilot instructions** in `.github/copilot-instructions.md`

---

**Made with ⚡ for electricians and engineers who value precision and efficiency.**
