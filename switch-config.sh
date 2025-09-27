#!/bin/bash

# HTTPS Configuration Switch Script
# Use this script to easily switch between HTTP and HTTPS development setups

FRONTEND_DIR="frontend"
ENV_FILE="$FRONTEND_DIR/.env.local"
ENV_HTTPS_FILE="$FRONTEND_DIR/.env.local.https"

function show_help() {
    echo "HTTPS Configuration Switch Script"
    echo "Usage: $0 [http|https]"
    echo ""
    echo "  http   - Switch to HTTP development setup (avoids certificate issues)"
    echo "  https  - Switch to HTTPS development setup (required for DigiKey OAuth)"
    echo ""
    echo "Current configuration:"
    if [[ -f "$ENV_FILE" ]]; then
        echo "  API URL: $(grep REACT_APP_API_BASE_URL $ENV_FILE | cut -d'=' -f2)"
        echo "  HTTPS: $(grep HTTPS= $ENV_FILE | cut -d'=' -f2)"
    else
        echo "  No configuration found"
    fi
}

function switch_to_http() {
    echo "Switching to HTTP development setup..."
    
    cat > "$ENV_FILE" << EOF
# Development environment configuration
# Set to false to use HTTP for both frontend and backend (avoids mixed content issues)
HTTPS=false
REACT_APP_API_BASE_URL=http://localhost:8000/api
EOF
    
    echo "✓ Switched to HTTP configuration"
    echo "  Frontend: http://localhost:3000"
    echo "  Backend API: http://localhost:8000/api"
    echo ""
    echo "Start servers with: 'Start Full Application' task in VS Code"
}

function switch_to_https() {
    echo "Switching to HTTPS development setup..."
    
    cat > "$ENV_FILE" << EOF
# HTTPS Development environment configuration for DigiKey OAuth
# Use this configuration when running both frontend and backend with HTTPS
HTTPS=true
REACT_APP_API_BASE_URL=https://localhost:8001/api
EOF
    
    echo "✓ Switched to HTTPS configuration"
    echo "  Frontend: https://localhost:3000"
    echo "  Backend API: https://localhost:8001/api"
    echo ""
    echo "Start servers with: 'Start Full Application (HTTPS)' task in VS Code"
    echo ""
    echo "Note: You may need to accept certificate warnings in your browser for localhost"
}

case "$1" in
    "http")
        switch_to_http
        ;;
    "https")
        switch_to_https
        ;;
    *)
        show_help
        ;;
esac