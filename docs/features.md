# Feature Model

## 1. Feature Overview

The Electrical Panel Configurator provides a comprehensive set of features for professional electrical panel design and configuration.

## 2. Core Features

### 2.1 Template Management System

#### 2.1.1 Panel Template Library
**Description**: Comprehensive library of pre-configured panel templates from electrical manufacturers.

**Key Features**:
- Hager Volta series consumer units (12-way, 18-way, 24-way, 36-way, 48-way)
- Complete specifications: model numbers, dimensions, electrical ratings
- Manufacturer and series organization
- Template versioning and lifecycle management

**User Workflow**:
1. Browse available panel templates by manufacturer/series
2. View detailed specifications (voltage, current, enclosure type)
3. Select template for new panel creation
4. Template automatically defines slot layout and constraints

#### 2.1.2 Device Template Catalog
**Description**: Extensive catalog of electrical device templates with professional specifications.

**Device Categories**:
- **Protection Devices**: MCBs (6A-32A, Type B/C curves), RCDs (30mA/100mA), RCBOs
- **Measurement Devices**: Smart meters with energy monitoring
- **Control Devices**: Contactors, timers, surge protection
- **Specialized Devices**: Multi-slot devices (RCBOs=2 slots, Smart meters=4 slots)

**Technical Specifications**:
- Current ratings and voltage ranges
- Breaking capacity and sensitivity settings
- Curve types and pole configurations
- Physical dimensions and slot requirements

**User Workflow**:
1. Filter device templates by category, manufacturer, current rating
2. View detailed device specifications and electrical characteristics
3. Drag devices from library to panel slots
4. System validates placement based on device requirements

### 2.2 Panel Configuration Workspace

#### 2.2.1 Visual Panel Designer
**Description**: Interactive drag-and-drop interface for configuring electrical panels.

**Key Features**:
- Grid-based visual representation matching real panel layout
- Real-time device placement validation
- Multi-slot device spanning with visual feedback
- Template-based slot generation and organization

**User Workflow**:
1. Create new panel from selected template
2. View auto-generated slot grid (rows × columns)
3. Drag devices from library to available slots
4. Configure device settings and labels
5. Validate placement against electrical requirements

#### 2.2.2 Device Placement Engine
**Description**: Intelligent validation system ensuring proper device placement.

**Validation Rules**:
- Slot availability checking before placement
- Multi-slot device consecutive positioning
- Electrical compatibility verification
- Current rating and voltage validation

**Placement Features**:
- Visual indicators for occupied/available slots
- Error feedback for invalid placements
- Automatic spanning for multi-slot devices
- Undo/redo functionality for placement actions

### 2.3 Panel Instance Management

#### 2.3.1 Panel Lifecycle Management
**Description**: Complete management of panel instances from creation to deployment.

**Instance Properties**:
- Panel identification (name, location, description)
- Installation tracking (dates, status, notes)
- Template relationship preservation
- Configuration history and versioning

**User Workflow**:
1. Create panel instance from template
2. Configure panel metadata (name, location)
3. Customize device placement and settings
4. Track installation progress and dates
5. Update and maintain panel configurations

#### 2.3.2 Device Instance Configuration
**Description**: Detailed configuration management for individual device instances.

**Configuration Options**:
- Custom device labeling and identification
- Current setting adjustments within device limits
- Installation date tracking
- Custom properties and notes

**Validation Features**:
- Current setting validation against device templates
- Electrical safety requirement checking
- Configuration conflict detection
- Standards compliance verification

### 2.4 Wiring and Connection Management

#### 2.4.1 Wire Connection System
**Description**: Comprehensive wiring management with electrical standards compliance.

**Connection Types**:
- Device-to-device connections within panel
- External source connections (supply, loads)
- Earth bonding and protection connections
- Control and monitoring circuits

**Wire Specifications**:
- Wire types (Live, Neutral, Earth, Control)
- Cross-sectional area selection
- Color coding per UK/EU standards
- Length calculations and material requirements

#### 2.4.2 Electrical Standards Integration
**Description**: Built-in compliance with UK/EU electrical regulations.

**Standards Features**:
- Automatic wire cross-section recommendations
- Current carrying capacity validation
- RCD protection requirement checking
- Earth fault protection compliance

**Color Standards**:
- Live: Brown (single phase), Brown/Black/Grey (three phase)
- Neutral: Blue
- Earth: Green/Yellow
- Control circuits: Various standard colors

### 2.5 User Interface Features

#### 2.5.1 Responsive Design System
**Description**: Modern, responsive interface optimized for professional use.

**Design Features**:
- Material-UI component library
- Responsive grid layouts
- Professional electrical industry styling
- Accessibility compliance (WCAG guidelines)

**Navigation**:
- Panel selector with template preview
- Device library with advanced filtering
- Panel workspace with tool palette
- Wiring view with connection visualization

#### 2.5.2 Interactive Components
**Description**: Rich interactive elements for efficient panel configuration.

**Interaction Features**:
- Drag-and-drop device placement
- Context menus for device configuration
- Real-time validation feedback
- Visual connection routing
- Zoom and pan for detailed work

### 2.6 Data Management Features

#### 2.6.1 Template vs Instance Architecture
**Description**: Clean separation between reusable templates and specific installations.

**Template Benefits**:
- Consistent device specifications across projects
- Manufacturer catalog integration
- Template updates don't affect existing panels
- Standardized component library

**Instance Benefits**:
- Project-specific customizations
- Installation tracking and history
- Customer and location specific data
- Configuration variations from templates

#### 2.6.2 Database Integration
**Description**: Robust data persistence with relationship integrity.

**Database Features**:
- SQLAlchemy ORM with relationship management
- Foreign key constraints ensuring data integrity
- Efficient querying with proper indexing
- Migration support for schema evolution

## 3. Advanced Features

### 3.1 Validation and Safety
- **Real-time Validation**: Immediate feedback on configuration errors
- **Safety Compliance**: Built-in electrical safety requirement checking
- **Standards Integration**: UK/EU electrical regulation compliance
- **Error Prevention**: Proactive validation prevents invalid configurations

### 3.2 Professional Integration
- **Manufacturer Catalogs**: Real device specifications from Hager catalog
- **Industry Standards**: Professional electrical terminology and symbols
- **Scalable Design**: Architecture supports additional manufacturers
- **Export Capabilities**: Future support for configuration export

### 3.3 Developer Experience
- **API Documentation**: Comprehensive OpenAPI/Swagger documentation
- **Type Safety**: Full TypeScript coverage on frontend
- **Code Quality**: Automated linting and formatting
- **Testing Framework**: Unit and integration test support

## 4. User Personas and Workflows

### 4.1 Electrical Engineer
**Primary Use Case**: Design electrical panels for new installations

**Typical Workflow**:
1. Select appropriate panel template for project requirements
2. Configure panel with required protection and measurement devices
3. Validate electrical compliance and safety requirements
4. Export configuration for installation documentation

### 4.2 Electrician
**Primary Use Case**: Configure panels for residential/commercial installations

**Typical Workflow**:
1. Choose panel template matching physical installation
2. Place MCBs, RCDs, and RCBOs based on circuit requirements
3. Configure device settings and circuit labeling
4. Verify wiring requirements and material specifications

### 4.3 Electrical Contractor
**Primary Use Case**: Manage multiple panel configurations across projects

**Typical Workflow**:
1. Create standardized panel templates for common installations
2. Customize panels for specific customer requirements
3. Track installation progress and completion dates
4. Maintain library of proven configurations

## 5. Future Feature Roadmap

### 5.1 Short-term Enhancements
- Additional manufacturer support (Schneider, ABB, Siemens)
- Export to common electrical CAD formats
- Load calculation and circuit analysis
- Advanced wiring diagram generation

### 5.2 Long-term Vision
- 3D panel visualization
- IoT device integration and monitoring
- Cloud-based configuration sharing
- Mobile application for field use

---

*Document Version: 1.0*  
*Last Updated: September 2025*