# Electrical Panel Configurator Documentation

Welcome to the comprehensive documentation for the Electrical Panel Configurator application.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Quick Start](#quick-start)
- [Documentation Sections](#documentation-sections)
- [Contributing](#contributing)

## 🔌 Project Overview

The Electrical Panel Configurator is a full-stack web application designed to help electricians, engineers, and electrical professionals configure electrical panels with proper device placement, wiring connections, and compliance with electrical standards.

### Key Capabilities

- **Template-Based Configuration**: Use pre-defined panel and device templates from manufacturers like Hager
- **Visual Panel Design**: Drag-and-drop interface for placing electrical devices in panel slots
- **Wiring Management**: Configure and visualize wire connections between devices
- **Standards Compliance**: Built-in validation for UK/EU electrical regulations
- **Professional Specifications**: Real-world device specifications including current ratings, breaking capacity, and safety features

### Technology Stack

- **Backend**: Python FastAPI with SQLAlchemy ORM and SQLite database
- **Frontend**: React with TypeScript, Material-UI, and React DnD
- **API**: RESTful API with automatic OpenAPI documentation

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- npm or yarn

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd x_panel_configurator_light
   ```

2. **Setup Backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Initialize Database**
   ```bash
   python init_sqlalchemy_db.py
   ```

4. **Start Backend Server**
   ```bash
   uvicorn main:app --reload --port 8000
   ```

5. **Setup Frontend**
   ```bash
   cd ../frontend
   npm install
   npm start
   ```

6. **Access Application**
   - Frontend: http://localhost:3000
   - API Documentation: http://localhost:8000/docs

## 📚 Documentation Sections

### [Requirements](./requirements.md)
Detailed functional and technical requirements covering:
- Template system architecture
- Panel configuration workflows  
- Device management and validation
- Wiring and electrical standards compliance

### [Feature Model](./features.md)
Comprehensive overview of implemented features:
- User workflows and use cases
- Feature descriptions and capabilities
- UI/UX design patterns

### [Software Architecture](./architecture.md)
Technical architecture documentation including:
- Domain model and class diagrams
- Component architecture and interactions
- Deployment and infrastructure diagrams
- Database schema and relationships

### [API Reference](./api.md)
Complete API documentation:
- Endpoint specifications
- Request/response schemas
- Authentication and error handling
- Integration examples

### [Developer Guide](./developer-guide.md)
Development and contribution guidelines:
- Project structure and conventions
- Development workflow
- Testing strategies
- Deployment procedures

## 🔧 Contributing

We welcome contributions! Please see our [Developer Guide](./developer-guide.md) for:
- Code style guidelines
- Development setup
- Testing requirements
- Pull request process

## 📞 Support

For questions, issues, or feature requests:
- Create an issue in the repository
- Review existing documentation
- Check the API documentation at `/docs` endpoint

---

*Last updated: September 2025*