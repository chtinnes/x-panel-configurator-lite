# Electrical Panel Configurator

A comprehensive web application for configuring electrical panels, specifically designed for Hager Volta panels. This tool allows users to design electrical installations with an intuitive drag-and-drop interface.

## Features

### Panel Configuration
- **Panel Templates**: Pre-configured Hager Volta panel templates (12, 18, 24 way)
- **Custom Panels**: Create custom panels with specific slot counts and ratings
- **Device Management**: Drag-and-drop devices from a comprehensive library
- **Multi-slot Devices**: Support for devices that span multiple slots (RCBOs, smart meters)

### Device Library
- **Circuit Breakers**: MCBs in various ratings (6A, 10A, 16A, 20A, 32A)
- **RCD/RCBO Protection**: Residual current devices with various ratings
- **Smart Devices**: Digital meters and monitoring equipment
- **Control Devices**: Contactors and switching equipment

### Wiring Configuration
- **Visual Wiring**: Configure connections between devices and external circuits
- **Wire Standards**: Built-in UK/EU wire color and cross-section standards
- **Wire Labeling**: Custom labels and tagging for all connections
- **Length Tracking**: Track wire lengths for material calculations

### Professional Features
- **Project Management**: Save and manage multiple panel configurations
- **Standards Compliance**: Built-in electrical standards and recommendations
- **Export Capabilities**: Generate documentation for installations

## Technology Stack

### Backend
- **FastAPI**: Modern, fast Python web framework
- **SQLAlchemy**: SQL toolkit and ORM
- **SQLite**: Lightweight database for development
- **Pydantic**: Data validation using Python type annotations

### Frontend
- **React**: User interface library with TypeScript
- **Material-UI**: Modern React UI framework
- **React DnD**: Drag and drop for React
- **Axios**: HTTP client for API communication

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 18+
- npm or yarn

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the development server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

The API will be available at `http://localhost:8000`

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

The application will be available at `http://localhost:3000`

## API Documentation

Once the backend is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Usage Guide

### Creating a Panel
1. Click "Create Panel" or "From Template" in the sidebar
2. Fill in panel details (name, model, slot count, ratings)
3. The panel slots will be automatically created

### Adding Devices
1. Browse the device library in the sidebar
2. Drag devices from the library to panel slots
3. Configure device settings (labels, current ratings)
4. Multi-slot devices will automatically span the required slots

### Configuring Wiring
1. Switch to the "Wiring Configuration" view
2. Click "Add Wire" to create connections
3. Select source and destination (slots or external connections)
4. Configure wire properties (type, color, cross-section)

### Panel Templates
Pre-configured templates include:
- **Hager Volta 12 Way (VD112)**: 63A rating, suitable for small homes
- **Hager Volta 18 Way (VD118)**: 100A rating, suitable for medium homes  
- **Hager Volta 24 Way (VD124)**: 100A rating, suitable for large homes

## Project Structure

```
├── backend/
│   ├── main.py              # FastAPI application
│   ├── models.py            # Database models
│   ├── schemas.py           # Pydantic schemas
│   ├── database.py          # Database configuration
│   ├── requirements.txt     # Python dependencies
│   └── routers/            # API route handlers
│       ├── panels.py
│       ├── devices.py
│       └── wiring.py
├── frontend/
│   ├── src/
│   │   ├── App.tsx          # Main application component
│   │   ├── components/      # React components
│   │   ├── services/        # API service layer
│   │   └── types/           # TypeScript type definitions
│   ├── public/
│   └── package.json
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Hager Group for electrical component specifications
- UK electrical standards and regulations
- React and Python communities for excellent frameworks and tools

## Support

For support and questions, please open an issue in the GitHub repository.
