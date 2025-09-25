# API Reference

## 1. Overview

The Electrical Panel Configurator provides a comprehensive REST API for managing panel templates, device templates, panel instances, and wiring configurations.

**Base URL**: `http://localhost:8000`  
**API Documentation**: `http://localhost:8000/docs` (Interactive Swagger UI)

## 2. Authentication

Currently, the API does not require authentication. Future versions will implement:
- JWT token-based authentication
- Role-based access control (Admin, Engineer, Technician)
- API key authentication for integrations

## 3. Template Management APIs

### 3.1 Panel Templates

#### Get Panel Templates
```http
GET /api/templates/panel-templates
```

**Query Parameters**:
- `manufacturer` (optional): Filter by manufacturer name
- `series` (optional): Filter by product series
- `active_only` (optional): Show only active templates (default: true)

**Response Example**:
```json
[
  {
    "id": 1,
    "name": "Hager Volta 12-way Consumer Unit",
    "model": "VML712",
    "manufacturer": "Hager",
    "series": "Volta",
    "rows": 2,
    "slots_per_row": 6,
    "voltage": 230.0,
    "max_current": 100.0,
    "enclosure_type": "Metal",
    "protection_rating": "IP30",
    "description": "Standard 12-way consumer unit for residential installations",
    "is_active": true,
    "total_slots": 12,
    "created_at": "2025-09-25T18:07:03",
    "updated_at": null
  }
]
```

#### Create Panel Template
```http
POST /api/templates/panel-templates
```

**Request Body**:
```json
{
  "name": "Custom Panel Template",
  "model": "CUSTOM-001",
  "manufacturer": "Hager",
  "series": "Custom",
  "rows": 3,
  "slots_per_row": 6,
  "voltage": 230.0,
  "max_current": 63.0,
  "enclosure_type": "Plastic",
  "protection_rating": "IP20",
  "description": "Custom panel template for specific installation"
}
```

### 3.2 Device Templates

#### Get Device Templates
```http
GET /api/templates/device-templates
```

**Query Parameters**:
- `manufacturer` (optional): Filter by manufacturer
- `series` (optional): Filter by product series
- `device_type` (optional): Filter by device type (MCB, RCD, RCBO, etc.)
- `category` (optional): Filter by category (Protection, Measurement, Control)
- `active_only` (optional): Show only active templates (default: true)

**Response Example**:
```json
[
  {
    "id": 1,
    "name": "Single Pole MCB 16A Type B",
    "model": "MTN116",
    "manufacturer": "Hager",
    "series": "MyTN",
    "device_type": "MCB",
    "category": "Protection",
    "slots_required": 1,
    "rated_current": 16.0,
    "max_current": 16.0,
    "voltage_range": "230V AC",
    "breaking_capacity": 6000.0,
    "sensitivity": null,
    "curve_type": "B",
    "pole_count": 1,
    "width_in_modules": 1.0,
    "features": null,
    "description": "16A Type B single pole MCB for socket outlets",
    "is_active": true,
    "created_at": "2025-09-25T18:07:03",
    "updated_at": null
  }
]
```

#### Get Device Library for Component Selection
```http
GET /api/templates/library/devices/{manufacturer}
```

**Path Parameters**:
- `manufacturer`: Manufacturer name (e.g., "Hager")

**Query Parameters**:
- `category` (optional): Filter by device category

## 4. Panel Management APIs

### 4.1 Panel Operations

#### Create Panel from Template
```http
POST /api/panels/
```

**Request Body**:
```json
{
  "name": "Main Distribution Panel",
  "template_id": 1,
  "location": "Electrical Room",
  "description": "Primary electrical distribution panel for building"
}
```

**Response**: Returns created panel with template information and auto-generated slots.

#### Get Panel with Slots
```http
GET /api/panels/{panel_id}
```

**Response Example**:
```json
{
  "id": 1,
  "name": "Main Distribution Panel",
  "template_id": 1,
  "location": "Electrical Room",
  "description": "Primary electrical distribution panel",
  "template": {
    "id": 1,
    "name": "Hager Volta 12-way Consumer Unit",
    "total_slots": 12
  },
  "slots": [
    {
      "id": 1,
      "slot_number": 1,
      "row": 1,
      "column": 1,
      "is_occupied": false,
      "device_template_id": null,
      "device_template": null
    }
  ]
}
```

## 5. Device Placement APIs

### 5.1 Slot Management

#### Place Device in Slot
```http
PUT /api/devices/slots/{slot_id}
```

**Request Body**:
```json
{
  "device_template_id": 5,
  "device_label": "Kitchen Lights",
  "current_setting": 10.0,
  "custom_properties": "{\"circuit_number\": \"L1\"}"
}
```

#### Check Device Placement Validity
```http
GET /api/devices/slots/{slot_id}/can-place/{device_template_id}
```

**Response**:
```json
{
  "can_place": true,
  "reason": "Placement valid",
  "required_slots": 1,
  "available_slots": 3
}
```

#### Remove Device from Slot
```http
DELETE /api/devices/slots/{slot_id}/device
```

## 6. Wiring Management APIs

### 6.1 Wire Operations

#### Create Wire Connection
```http
POST /api/wiring/
```

**Request Body**:
```json
{
  "panel_id": 1,
  "label": "L1 Supply",
  "wire_type": "Live",
  "cross_section": 2.5,
  "color": "Brown",
  "source_slot_id": 1,
  "destination_slot_id": 5,
  "length": 0.5
}
```

#### Get Panel Wiring
```http
GET /api/wiring/panel/{panel_id}
```

### 6.2 Standards Information

#### Get Wire Color Standards
```http
GET /api/wiring/standards/colors
```

**Response**:
```json
{
  "live_single": "Brown",
  "live_three_phase": ["Brown", "Black", "Grey"],
  "neutral": "Blue",
  "earth": "Green/Yellow",
  "control": ["White", "Yellow", "Pink", "Orange"]
}
```

#### Get Wire Cross-Section Standards
```http
GET /api/wiring/standards/cross-sections
```

**Response**:
```json
{
  "current_ratings": {
    "1.0": {"max_current": 10, "applications": ["Lighting"]},
    "1.5": {"max_current": 15, "applications": ["Lighting, Small appliances"]},
    "2.5": {"max_current": 20, "applications": ["Socket outlets"]},
    "4.0": {"max_current": 25, "applications": ["Cookers, Showers"]},
    "6.0": {"max_current": 32, "applications": ["Electric showers, Cookers"]}
  }
}
```

## 7. Error Handling

### 7.1 HTTP Status Codes

- **200 OK**: Request successful
- **201 Created**: Resource created successfully
- **400 Bad Request**: Invalid request data
- **404 Not Found**: Resource not found
- **422 Unprocessable Entity**: Validation error
- **500 Internal Server Error**: Server error

### 7.2 Error Response Format

```json
{
  "detail": [
    {
      "loc": ["body", "template_id"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 7.3 Common Error Scenarios

#### Validation Errors
- Missing required fields
- Invalid data types
- Out-of-range values

#### Business Logic Errors
- Invalid device placement (insufficient slots)
- Template not found
- Electrical validation failures

## 8. Request/Response Examples

### 8.1 Complete Panel Configuration Workflow

1. **Get Available Templates**:
```bash
curl "http://localhost:8000/api/templates/panel-templates?manufacturer=Hager"
```

2. **Create Panel from Template**:
```bash
curl -X POST "http://localhost:8000/api/panels/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Kitchen Panel", "template_id": 1, "location": "Kitchen"}'
```

3. **Get Device Templates**:
```bash
curl "http://localhost:8000/api/templates/library/devices/Hager?category=Protection"
```

4. **Place Device in Slot**:
```bash
curl -X PUT "http://localhost:8000/api/devices/slots/1" \
  -H "Content-Type: application/json" \
  -d '{"device_template_id": 5, "device_label": "Kitchen Lights", "current_setting": 10.0}'
```

### 8.2 Validation Example

**Invalid Device Placement**:
```bash
curl -X PUT "http://localhost:8000/api/devices/slots/1" \
  -H "Content-Type: application/json" \
  -d '{"device_template_id": 999, "current_setting": 50.0}'
```

**Response**:
```json
{
  "detail": "Device template not found or current setting exceeds device limits"
}
```

## 9. Integration Guidelines

### 9.1 Best Practices

- **Always validate device placement** before attempting to place devices
- **Use template IDs consistently** when creating panels and placing devices  
- **Check electrical standards** when configuring wiring
- **Handle errors gracefully** with proper error messages to users

### 9.2 Rate Limiting

Current implementation has no rate limiting. Production deployment should implement:
- 100 requests/minute per IP for template queries
- 50 requests/minute per IP for panel modifications
- 200 requests/minute per IP for read operations

### 9.3 Caching Strategy

- Template data: Cache for 1 hour (rarely changes)
- Panel configurations: No caching (frequently modified)
- Standards data: Cache for 24 hours (static information)

---

*Document Version: 1.0*  
*Last Updated: September 2025*