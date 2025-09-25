# Requirements Specification

## 1. Overview

The Electrical Panel Configurator enables professional electrical panel configuration with template-based design, device placement validation, and compliance with electrical standards.

## 2. Functional Requirements

### 2.1 Template System Management

#### 2.1.1 Panel Templates
- **FR-PT-01**: System SHALL provide predefined panel templates from manufacturers (Hager Volta series)
- **FR-PT-02**: Templates SHALL include specifications: model, manufacturer, dimensions (rows x slots), voltage, max current, enclosure type, protection rating
- **FR-PT-03**: System SHALL support CRUD operations for panel templates via API
- **FR-PT-04**: Templates SHALL be filterable by manufacturer, series, and active status

#### 2.1.2 Device Templates  
- **FR-DT-01**: System SHALL provide comprehensive device template library (MCBs, RCDs, RCBOs, Smart Meters, etc.)
- **FR-DT-02**: Device templates SHALL include: name, model, manufacturer, device type, current ratings, voltage range, breaking capacity, sensitivity, curve type, slot requirements
- **FR-DT-03**: System SHALL support device template categorization (Protection, Measurement, Control)
- **FR-DT-04**: Templates SHALL be filterable by manufacturer, series, device type, category, and current rating

### 2.2 Panel Configuration

#### 2.2.1 Panel Instance Management
- **FR-PI-01**: Users SHALL create panel instances from templates
- **FR-PI-02**: Panel instances SHALL inherit template specifications and auto-generate slot layout
- **FR-PI-03**: System SHALL support panel metadata: name, location, installation date, description
- **FR-PI-04**: System SHALL maintain relationship between panel instances and their source templates

#### 2.2.2 Slot Management
- **FR-SM-01**: System SHALL automatically create slots based on panel template dimensions
- **FR-SM-02**: Each slot SHALL have position coordinates (row, column, slot_number)
- **FR-SM-03**: Slots SHALL support device placement with template reference
- **FR-SM-04**: System SHALL track slot occupancy and spanning (multi-slot devices)

### 2.3 Device Placement and Validation

#### 2.3.1 Device Placement
- **FR-DP-01**: Users SHALL place devices by dragging from template library to panel slots
- **FR-DP-02**: System SHALL validate device placement based on slot availability and device slot requirements
- **FR-DP-03**: Multi-slot devices (RCBOs=2 slots, Smart Meters=4 slots) SHALL span consecutive slots
- **FR-DP-04**: System SHALL prevent overlapping device placement

#### 2.3.2 Device Configuration
- **FR-DC-01**: Users SHALL configure device settings: custom labels, current settings
- **FR-DC-02**: System SHALL validate current settings against device template specifications
- **FR-DC-03**: System SHALL track installation dates and custom properties per device instance

### 2.4 Wiring Management

#### 2.4.1 Wire Connections
- **FR-WC-01**: System SHALL support wire connections between panel slots
- **FR-WC-02**: Users SHALL configure wire properties: type, cross-section, color, length
- **FR-WC-03**: System SHALL validate wire cross-sections against current requirements
- **FR-WC-04**: System SHALL support external connections (to/from external sources)

#### 2.4.2 Electrical Standards
- **FR-ES-01**: System SHALL provide standard wire colors according to UK/EU regulations
- **FR-ES-02**: System SHALL recommend appropriate wire cross-sections for device current ratings
- **FR-ES-03**: System SHALL validate electrical safety requirements (RCD protection, current ratings)

### 2.5 User Interface

#### 2.5.1 Panel View
- **FR-UI-01**: System SHALL provide visual panel representation with grid layout
- **FR-UI-02**: Users SHALL see device placement with proper visual representation
- **FR-UI-03**: Interface SHALL show panel template information and specifications
- **FR-UI-04**: System SHALL provide device placement validation feedback

#### 2.5.2 Device Library
- **FR-UI-05**: System SHALL provide searchable device library with template specifications
- **FR-UI-06**: Library SHALL display device categories, manufacturers, and current ratings
- **FR-UI-07**: Users SHALL filter devices by type, manufacturer, and current rating
- **FR-UI-08**: System SHALL show device availability and slot requirements

#### 2.5.3 Wiring View
- **FR-UI-09**: System SHALL provide wiring diagram view showing connections
- **FR-UI-10**: Users SHALL visualize wire routes and connection points
- **FR-UI-11**: Interface SHALL display wire specifications and color coding

## 3. Technical Requirements

### 3.1 Performance
- **NFR-P-01**: API response time SHALL be < 200ms for CRUD operations
- **NFR-P-02**: System SHALL support concurrent users (minimum 10)
- **NFR-P-03**: Database queries SHALL be optimized with appropriate indexing

### 3.2 Scalability
- **NFR-S-01**: Template library SHALL support 500+ device templates
- **NFR-S-02**: System SHALL handle 100+ panel configurations per user
- **NFR-S-03**: Database SHALL support efficient template-to-instance relationships

### 3.3 Data Integrity
- **NFR-D-01**: System SHALL maintain referential integrity between templates and instances
- **NFR-D-02**: Database SHALL prevent orphaned slot and device records
- **NFR-D-03**: Template modifications SHALL not affect existing panel instances

### 3.4 Security
- **NFR-SEC-01**: API SHALL validate all input parameters
- **NFR-SEC-02**: System SHALL prevent SQL injection and XSS attacks
- **NFR-SEC-03**: Database access SHALL use parameterized queries

### 3.5 Maintainability
- **NFR-M-01**: Code SHALL follow established style guidelines (PEP 8 for Python, ESLint for TypeScript)
- **NFR-M-02**: System SHALL have comprehensive API documentation (OpenAPI/Swagger)
- **NFR-M-03**: Database schema SHALL support version migration scripts

## 4. Constraints and Assumptions

### 4.1 Technical Constraints
- **TC-01**: Backend SHALL use Python FastAPI framework
- **TC-02**: Frontend SHALL use React with TypeScript
- **TC-03**: Database SHALL use SQLite for development (SQLAlchemy ORM)
- **TC-04**: API SHALL follow REST architectural principles

### 4.2 Business Constraints
- **BC-01**: Initial focus on Hager manufacturer devices and panels
- **BC-02**: Electrical standards SHALL comply with UK/EU regulations (17th/18th Edition)
- **BC-03**: Professional use targeting electricians and electrical engineers

### 4.3 Assumptions
- **AS-01**: Users have basic electrical knowledge and understanding of panel configurations
- **AS-02**: Device templates represent real-world specifications from manufacturer catalogs
- **AS-03**: Panel configurations will be used for planning purposes (not live electrical control)

## 5. Success Criteria

### 5.1 Functional Success
- **SC-F-01**: Users can successfully create panels from templates within 2 minutes
- **SC-F-02**: Device placement validation prevents 100% of invalid configurations
- **SC-F-03**: Template library provides comprehensive coverage of common electrical devices
- **SC-F-04**: Wiring configuration supports typical residential/commercial panel requirements

### 5.2 Technical Success
- **SC-T-01**: System maintains 99.5% uptime during development
- **SC-T-02**: Database operations complete within performance requirements
- **SC-T-03**: API documentation covers 100% of endpoints with examples
- **SC-T-04**: Frontend responsive design works on desktop and tablet devices

---

*Document Version: 1.0*  
*Last Updated: September 2025*