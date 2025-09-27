#!/usr/bin/env python3
"""
DigiKey Integration Demo Script
Demonstrates how to use the DigiKey API integration for template synchronization
"""

import sys
import os
import requests
import json
import time
from datetime import datetime

# Add backend to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/template-sync"

def print_header(title):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)

def print_step(step_num, title):
    """Print a formatted step"""
    print(f"\n📋 Step {step_num}: {title}")
    print('-' * 50)

def make_request(method, endpoint, data=None):
    """Make API request with error handling"""
    url = f"{API_BASE}{endpoint}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url)
        elif method.upper() == "POST":
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, json=data, headers=headers)
        
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        if hasattr(e.response, 'text'):
            print(f"   Response: {e.response.text}")
        return None

def check_server_running():
    """Check if the backend server is running"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def demo_integration():
    """Run the DigiKey integration demo"""
    
    print_header("DigiKey API Integration Demo")
    print(f"Demo started at: {datetime.now()}")
    
    # Check server status
    print_step(1, "Check Backend Server")
    if not check_server_running():
        print("❌ Backend server is not running!")
        print("   Please start it with: cd backend && uvicorn main:app --reload --port 8000")
        return False
    print("✅ Backend server is running")
    
    # Check demo endpoint
    print_step(2, "Check Integration Status")
    demo_status = make_request("GET", "/demo")
    if demo_status:
        print(f"✅ Integration Status:")
        print(f"   API Configured: {demo_status.get('api_configured', False)}")
        print(f"   Message: {demo_status.get('message', 'Unknown')}")
        
        if demo_status.get('authentication_url'):
            print(f"   🔗 Auth URL: {demo_status['authentication_url'][:60]}...")
    else:
        print("❌ Failed to get demo status")
        return False
    
    # Check API status
    print_step(3, "Check API Configuration")
    status = make_request("GET", "/status")
    if status:
        print(f"✅ API Status:")
        print(f"   API Configured: {status.get('api_configured', False)}")
        print(f"   Authenticated: {status.get('authenticated', False)}")
        print(f"   Sandbox Mode: {status.get('sandbox_mode', True)}")
        print(f"   Sync Service Ready: {status.get('sync_service_ready', False)}")
        
        if not status.get('api_configured'):
            print("\n⚠️  API not configured. You need to:")
            print("   1. Set DIGIKEY_CLIENT_ID environment variable")
            print("   2. Set DIGIKEY_CLIENT_SECRET environment variable")
            print("   3. Get credentials from https://developer.digikey.com/")
    else:
        print("❌ Failed to get API status")
        return False
    
    # Get supported manufacturers
    print_step(4, "Get Supported Manufacturers")
    manufacturers = make_request("GET", "/supported-manufacturers")
    if manufacturers:
        print("✅ Supported Manufacturers:")
        for mfg in manufacturers.get('manufacturers', []):
            print(f"   • {mfg}")
        print(f"\nSupported Component Types:")
        for comp_type in manufacturers.get('component_types', []):
            print(f"   • {comp_type}")
    
    # Initialize panel templates
    print_step(5, "Initialize Panel Templates")
    panel_result = make_request("POST", "/init-panels")
    if panel_result:
        print(f"✅ Panel Templates:")
        print(f"   Status: {panel_result.get('status', 'unknown')}")
        print(f"   Message: {panel_result.get('message', 'No message')}")
        if panel_result.get('results'):
            templates_added = panel_result['results'].get('panel_templates_added', 0)
            print(f"   Templates Added: {templates_added}")
    else:
        print("❌ Failed to initialize panel templates")
    
    # Check authentication requirement
    if not status.get('authenticated'):
        print_step(6, "Authentication Required")
        print("⚠️  To sync device templates, you need to authenticate:")
        print("   1. Get auth URL: curl http://localhost:8000/api/template-sync/auth-url")
        print("   2. Visit the URL and authorize")
        print("   3. Get auth code from callback")
        print("   4. Authenticate: curl -X POST http://localhost:8000/api/template-sync/authenticate \\")
        print("      -H 'Content-Type: application/json' \\")
        print("      -d '{\"authorization_code\": \"your_code\"}'")
        print("\n   Then you can sync templates:")
        print("   curl -X POST http://localhost:8000/api/template-sync/sync/Hager")
    else:
        print_step(6, "Sync Device Templates (Authenticated)")
        print("🚀 You can now sync device templates!")
        
        # Try syncing a small batch
        sync_data = {
            "manufacturers": ["Hager"],
            "component_types": ["circuit_breakers"]
        }
        
        print(f"   Attempting to sync: {sync_data}")
        sync_result = make_request("POST", "/sync", sync_data)
        
        if sync_result:
            print(f"✅ Sync Results:")
            print(f"   Status: {sync_result.get('status', 'unknown')}")
            print(f"   Message: {sync_result.get('message', 'No message')}")
            
            if sync_result.get('results'):
                for mfg, result in sync_result['results'].items():
                    if isinstance(result, dict):
                        new = result.get('new_templates', 0)
                        updated = result.get('updated_templates', 0)
                        errors = result.get('errors', 0)
                        print(f"   {mfg}: {new} new, {updated} updated, {errors} errors")
        else:
            print("❌ Failed to sync templates")
    
    # Summary
    print_header("Demo Summary")
    print("✅ DigiKey integration is ready!")
    print("\nWhat you can do now:")
    print("• Use the FastAPI docs at http://localhost:8000/docs")
    print("• Configure DigiKey API credentials if needed")
    print("• Authenticate and start syncing real component data")
    print("• Build your frontend integration")
    
    print(f"\nDemo completed at: {datetime.now()}")
    return True

if __name__ == "__main__":
    print("🔌 Starting DigiKey Integration Demo...")
    success = demo_integration()
    
    if success:
        print("\n🎉 Demo completed successfully!")
    else:
        print("\n❌ Demo encountered issues.")
        sys.exit(1)