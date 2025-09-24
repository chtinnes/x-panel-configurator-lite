<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Electrical Panel Configurator - Copilot Instructions

This is a full-stack electrical panel configurator application designed primarily for Hager Volta electrical panels.

## Project Context

This application helps electricians and engineers configure electrical panels by:
- Selecting from pre-configured panel templates (Hager Volta series)
- Dragging and dropping electrical devices (MCBs, RCDs, RCBOs, smart meters) into panel slots
- Configuring wiring connections between devices
- Managing device settings like current ratings and labels
- Following UK/EU electrical standards for wire colors and cross-sections

## Architecture

- **Backend**: Python FastAPI with SQLAlchemy ORM and SQLite database
- **Frontend**: React with TypeScript, Material-UI, and React DnD for drag-and-drop
- **API**: RESTful API with automatic OpenAPI documentation

## Key Concepts

### Electrical Terms
- **MCB**: Miniature Circuit Breaker (protection device)
- **RCD**: Residual Current Device (earth leakage protection)
- **RCBO**: Combined MCB + RCD in one device (requires 2 slots)
- **Smart Meter**: Digital electricity meter (requires 4 slots)
- **Panel Slots**: Physical positions in the electrical panel where devices are mounted

### Device Specifications
- Devices have current ratings (6A, 10A, 16A, 20A, 32A, etc.)
- Some devices span multiple slots (RCBOs = 2 slots, Smart meters = 4 slots)
- Wire cross-sections must match device current ratings for safety

## Code Patterns

### Backend (FastAPI)
- Use Pydantic schemas for request/response validation
- SQLAlchemy models for database entities
- Router-based organization for different endpoints
- Dependency injection for database sessions

### Frontend (React + TypeScript)
- Material-UI components for consistent UI
- React DnD for drag-and-drop functionality
- Axios for API communication
- TypeScript interfaces matching backend schemas

## Standards and Safety

When working with electrical components, always consider:
- UK electrical regulations (17th/18th Edition wiring regulations)
- Proper current ratings and wire cross-sections
- RCD protection requirements (30mA for socket outlets)
- Proper earthing and bonding
- Load balancing across phases

## Development Guidelines

- Follow electrical industry terminology accurately
- Ensure all current ratings and specifications are realistic
- Validate that wire cross-sections match current ratings
- Use proper electrical symbols and colors in the UI
- Maintain data consistency between frontend and backend
