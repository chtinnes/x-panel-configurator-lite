# Developer Guide

## 1. Getting Started

### 1.1 Prerequisites

- **Python 3.9+** with pip
- **Node.js 16+** with npm or yarn
- **Git** for version control
- **VS Code** (recommended IDE)

### 1.2 Development Environment Setup

#### Clone and Setup
```bash
# Clone repository
git clone <repository-url>
cd x_panel_configurator_light

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Initialize database
python init_sqlalchemy_db.py

# Frontend setup
cd ../frontend
npm install
```

#### Development Servers
```bash
# Terminal 1: Backend (from backend/)
uvicorn main:app --reload --port 8000

# Terminal 2: Frontend (from frontend/)
npm start
```

**Access Points**:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## 2. Project Structure

```
x_panel_configurator_light/
├── backend/                 # Python FastAPI backend
│   ├── main.py             # FastAPI application entry point
│   ├── database.py         # Database configuration and session
│   ├── models.py           # SQLAlchemy database models
│   ├── schemas.py          # Pydantic request/response schemas
│   ├── requirements.txt    # Python dependencies
│   ├── routers/           # API route modules
│   │   ├── panels.py      # Panel management endpoints
│   │   ├── devices.py     # Device placement endpoints
│   │   ├── templates.py   # Template management endpoints
│   │   └── wiring.py      # Wiring configuration endpoints
│   └── init_sqlalchemy_db.py  # Database initialization script
├── frontend/               # React TypeScript frontend
│   ├── src/
│   │   ├── App.tsx        # Main application component
│   │   ├── types/         # TypeScript type definitions
│   │   ├── components/    # React components
│   │   │   ├── PanelSelector.tsx    # Panel template selection
│   │   │   ├── PanelView.tsx        # Panel configuration workspace
│   │   │   ├── DeviceLibrary.tsx    # Device template library
│   │   │   └── WiringView.tsx       # Wiring configuration
│   │   └── services/      # API client services
│   ├── package.json       # Frontend dependencies
│   └── tsconfig.json      # TypeScript configuration
├── docs/                  # Project documentation
│   ├── README.md          # Main documentation
│   ├── requirements.md    # Requirements specification
│   ├── features.md        # Feature documentation
│   ├── architecture.md    # Software architecture
│   ├── api.md            # API reference
│   └── developer-guide.md # This guide
└── README.md             # Project overview
```

## 3. Development Workflow

### 3.1 Code Style and Standards

#### Python (Backend)
- **Style Guide**: PEP 8
- **Formatter**: Black (automatic formatting)
- **Linter**: Flake8 or Pylint
- **Type Hints**: Use Python type hints throughout
- **Docstrings**: Google-style docstrings for functions and classes

```python
def create_panel(panel_data: PanelCreate, db: Session) -> Panel:
    """Create a new panel instance from a template.
    
    Args:
        panel_data: Panel creation data including template_id
        db: Database session
        
    Returns:
        Created panel instance with auto-generated slots
        
    Raises:
        HTTPException: If template not found or validation fails
    """
    pass
```

#### TypeScript (Frontend)
- **Style Guide**: ESLint with recommended TypeScript rules
- **Formatter**: Prettier
- **Type Safety**: Strict TypeScript configuration
- **Component Style**: Functional components with hooks

```typescript
interface PanelProps {
  panel: PanelWithSlots;
  onDevicePlaced: (slotId: number, deviceTemplateId: number) => void;
}

const PanelView: React.FC<PanelProps> = ({ panel, onDevicePlaced }) => {
  // Implementation
};
```

### 3.2 Git Workflow

#### Branch Strategy
- `main`: Production-ready code
- `develop`: Integration branch for features
- `feature/description`: Individual feature branches
- `hotfix/description`: Critical bug fixes

#### Commit Messages
```
type(scope): brief description

Detailed description if needed

- feat: New feature
- fix: Bug fix
- docs: Documentation changes
- style: Formatting changes
- refactor: Code refactoring
- test: Adding tests
- chore: Maintenance tasks
```

**Examples**:
```
feat(templates): add device template filtering by category
fix(panels): resolve slot generation for custom panel sizes
docs(api): update panel creation endpoint documentation
```

### 3.3 Testing Strategy

#### Backend Testing
```python
# tests/test_panels.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_panel_from_template():
    response = client.post("/api/panels/", json={
        "name": "Test Panel",
        "template_id": 1,
        "location": "Test Location"
    })
    assert response.status_code == 200
    assert response.json()["template_id"] == 1
```

#### Frontend Testing
```typescript
// components/__tests__/PanelView.test.tsx
import { render, screen } from '@testing-library/react';
import { PanelView } from '../PanelView';

test('renders panel with correct slot count', () => {
  const mockPanel = {
    id: 1,
    name: 'Test Panel',
    template: { total_slots: 12 },
    slots: Array.from({ length: 12 }, (_, i) => ({ id: i + 1 }))
  };
  
  render(<PanelView panel={mockPanel} onDevicePlaced={() => {}} />);
  expect(screen.getAllByTestId('panel-slot')).toHaveLength(12);
});
```

#### Test Commands
```bash
# Backend tests
cd backend
python -m pytest tests/ -v

# Frontend tests  
cd frontend
npm test
```

## 4. Database Development

### 4.1 Model Development

#### Creating New Models
```python
# models.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class NewEntity(Base):
    __tablename__ = "new_entities"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey("parent_entities.id"))
    
    # Relationships
    parent = relationship("ParentEntity", back_populates="children")
```

#### Schema Definition
```python
# schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NewEntityBase(BaseModel):
    name: str
    parent_id: Optional[int] = None

class NewEntityCreate(NewEntityBase):
    pass

class NewEntity(NewEntityBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
```

### 4.2 Database Migrations

#### Adding New Tables
```python
# migrations/add_new_entity.py
import sqlite3

def migrate():
    conn = sqlite3.connect("panel_configurator.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE new_entities (
            id INTEGER PRIMARY KEY,
            name VARCHAR NOT NULL,
            parent_id INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(parent_id) REFERENCES parent_entities (id)
        )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    migrate()
```

#### Reinitializing Database
```bash
# Complete database recreation
cd backend
rm panel_configurator.db
python init_sqlalchemy_db.py
```

## 5. API Development

### 5.1 Adding New Endpoints

#### Router Structure
```python
# routers/new_feature.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import NewEntityCreate, NewEntity

router = APIRouter()

@router.post("/", response_model=NewEntity)
def create_entity(entity_data: NewEntityCreate, db: Session = Depends(get_db)):
    """Create a new entity."""
    # Implementation
    pass

@router.get("/{entity_id}", response_model=NewEntity)
def get_entity(entity_id: int, db: Session = Depends(get_db)):
    """Get entity by ID."""
    # Implementation
    pass
```

#### Registering Routes
```python
# main.py
from routers import new_feature

app.include_router(
    new_feature.router, 
    prefix="/api/new-feature", 
    tags=["new-feature"]
)
```

### 5.2 Error Handling

#### Custom Exceptions
```python
from fastapi import HTTPException

def validate_entity_exists(entity_id: int, db: Session):
    entity = db.query(Entity).filter(Entity.id == entity_id).first()
    if not entity:
        raise HTTPException(
            status_code=404, 
            detail=f"Entity {entity_id} not found"
        )
    return entity
```

#### Validation
```python
from pydantic import validator

class EntityCreate(BaseModel):
    name: str
    current_rating: float
    
    @validator('current_rating')
    def validate_current_rating(cls, v):
        if v <= 0 or v > 100:
            raise ValueError('Current rating must be between 0 and 100')
        return v
```

## 6. Frontend Development

### 6.1 Component Development

#### Component Structure
```typescript
// components/NewComponent.tsx
import React, { useState, useEffect } from 'react';
import { Box, Typography, Button } from '@mui/material';
import { apiService } from '../services/api';

interface NewComponentProps {
  data: SomeData;
  onAction: (id: number) => void;
}

export const NewComponent: React.FC<NewComponentProps> = ({ data, onAction }) => {
  const [state, setState] = useState<SomeState>(initialState);
  
  useEffect(() => {
    // Side effects
  }, [data]);
  
  const handleAction = () => {
    onAction(data.id);
  };
  
  return (
    <Box>
      <Typography variant="h6">{data.name}</Typography>
      <Button onClick={handleAction}>Action</Button>
    </Box>
  );
};
```

#### Type Definitions
```typescript
// types/index.ts
export interface PanelTemplate {
  id: number;
  name: string;
  model: string;
  manufacturer: string;
  total_slots: number;
  // ... other fields
}

export interface DeviceTemplate {
  id: number;
  name: string;
  device_type: string;
  category: string;
  slots_required: number;
  // ... other fields
}
```

### 6.2 API Integration

#### Service Layer
```typescript
// services/api.ts
const API_BASE = 'http://localhost:8000/api';

class ApiService {
  async getPanelTemplates(): Promise<PanelTemplate[]> {
    const response = await fetch(`${API_BASE}/templates/panel-templates`);
    if (!response.ok) throw new Error('Failed to fetch panel templates');
    return response.json();
  }
  
  async createPanel(panelData: PanelCreate): Promise<Panel> {
    const response = await fetch(`${API_BASE}/panels/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(panelData)
    });
    if (!response.ok) throw new Error('Failed to create panel');
    return response.json();
  }
}

export const apiService = new ApiService();
```

## 7. Debugging and Troubleshooting

### 7.1 Common Issues

#### Database Connection Issues
```python
# Check database file exists
import os
print(os.path.exists('panel_configurator.db'))

# Test database connection
from database import engine, SessionLocal
db = SessionLocal()
print(db.query(PanelTemplate).count())
db.close()
```

#### API CORS Issues
```python
# main.py - Ensure CORS is properly configured
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### Frontend API Connection
```typescript
// Check API connectivity
fetch('http://localhost:8000/health')
  .then(response => response.json())
  .then(data => console.log('API Status:', data))
  .catch(error => console.error('API Error:', error));
```

### 7.2 Development Tools

#### Backend Debugging
- **FastAPI Debug Mode**: `uvicorn main:app --reload --log-level debug`
- **Database Inspection**: Use SQLite browser or `sqlite3` CLI
- **API Testing**: Use `curl`, Postman, or FastAPI docs interface

#### Frontend Debugging
- **React DevTools**: Browser extension for component inspection
- **Network Tab**: Monitor API requests/responses
- **Console Logging**: Strategic logging for state changes

## 8. Deployment

### 8.1 Production Preparation

#### Environment Configuration
```python
# config.py
import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./panel_configurator.db"
    cors_origins: str = "http://localhost:3000"
    debug: bool = False
    
    class Config:
        env_file = ".env"

settings = Settings()
```

#### Environment Files
```bash
# .env
DATABASE_URL=postgresql://user:password@localhost/panel_configurator
CORS_ORIGINS=https://yourdomain.com
DEBUG=false
```

### 8.2 Docker Configuration

```dockerfile
# Dockerfile.backend
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```dockerfile
# Dockerfile.frontend  
FROM node:16
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
CMD ["npm", "start"]
```

## 9. Performance Optimization

### 9.1 Backend Optimization
- **Database Indexing**: Add indexes on frequently queried columns
- **Query Optimization**: Use SQLAlchemy eager loading
- **Caching**: Implement template data caching
- **Connection Pooling**: Configure SQLAlchemy connection pool

### 9.2 Frontend Optimization
- **Code Splitting**: Use React lazy loading
- **Memoization**: React.memo for expensive components
- **Bundle Analysis**: Use webpack-bundle-analyzer
- **State Management**: Minimize unnecessary re-renders

## 10. Contributing Guidelines

### 10.1 Before Contributing
1. Read this developer guide thoroughly
2. Set up development environment
3. Run existing tests to ensure everything works
4. Create feature branch from `develop`

### 10.2 Pull Request Process
1. **Test**: Ensure all tests pass
2. **Document**: Update relevant documentation
3. **Code Review**: Request review from maintainers
4. **Integration**: Merge to `develop` after approval

### 10.3 Issue Reporting
Include:
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, Node version)
- Error logs and stack traces

---

*Document Version: 1.0*  
*Last Updated: September 2025*