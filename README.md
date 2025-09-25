# Electrical Panel Configurator

A full-stack web application for configuring electrical panels, specifically designed for Hager Volta electrical panel series. This tool helps electricians and engineers design electrical installations by providing an intuitive drag-and-drop interface for placing devices and configuring wiring connections.

![Project Status](https://img.shields.io/badge/Status-Functional-brightgreen)
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

### Start Both Servers

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd electrical-panel-configurator
   ```

2. **Backend Setup**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn main:app --reload --port 8000
   ```

3. **Frontend Setup** (in a new terminal):
   ```bash
   cd frontend
   npm install
   npm start
   ```

4. **Access the Application**:
   - **Frontend**: http://localhost:3000
   - **API Documentation**: http://localhost:8000/docs
   - **Alternative API Docs**: http://localhost:8000/redoc

## 🏗️ Technology Stack

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
│   └── routers/                # API route handlers
│       ├── panels.py           # Panel management
│       ├── devices.py          # Device library
│       └── wiring.py           # Wiring configuration
├── frontend/                   # React TypeScript frontend
│   ├── public/
│   ├── src/
│   │   ├── App.tsx             # Main application
│   │   ├── components/         # React components
│   │   │   ├── PanelSelector.tsx
│   │   │   ├── PanelView.tsx
│   │   │   ├── DeviceLibrary.tsx
│   │   │   └── WiringView.tsx
│   │   ├── services/
│   │   │   └── api.ts          # API service layer
│   │   └── types/
│   │       └── index.ts        # TypeScript definitions
│   ├── package.json
│   └── tsconfig.json
└── README.md
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
1. **Ctrl/Cmd + Shift + P** → "Tasks: Run Task"
2. Select "Start Backend Server" and "Start Frontend Server"

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

1. **Frontend won't start**:
   ```bash
   cd frontend
   rm -rf node_modules package-lock.json
   npm install
   npm start
   ```

2. **Backend API errors**:
   ```bash
   cd backend
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Database issues**:
   ```bash
   cd backend
   rm panel_configurator.db  # Reset database
   # Restart backend to recreate with sample data
   ```

4. **CORS issues**:
   - Ensure backend runs on port 8000
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
