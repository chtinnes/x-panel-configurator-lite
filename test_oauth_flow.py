#!/usr/bin/env python3
"""
Test script for DigiKey OAuth flow
"""

import requests
import webbrowser
import json
from urllib.parse import urlparse, parse_qs

def test_oauth_flow():
    """Test the complete OAuth flow"""
    base_url = "http://localhost:8000"
    
    print("🔍 Testing DigiKey OAuth Flow...")
    
    # Step 1: Get API status
    print("\n1️⃣ Checking API status...")
    try:
        response = requests.get(f"{base_url}/api/template-sync/status")
        status = response.json()
        print(f"   API Configured: {status['api_configured']}")
        print(f"   Authenticated: {status['authenticated']}")
        print(f"   Sandbox Mode: {status['sandbox_mode']}")
        
        if not status['api_configured']:
            print("❌ API not configured. Check environment variables.")
            return
            
    except Exception as e:
        print(f"❌ Failed to get status: {e}")
        return
    
    # Step 2: Get authorization URL
    print("\n2️⃣ Getting authorization URL...")
    try:
        response = requests.get(f"{base_url}/api/template-sync/auth-url")
        auth_data = response.json()
        auth_url = auth_data['authorization_url']
        print(f"   Authorization URL: {auth_url}")
        
        # Parse the URL to show components
        parsed = urlparse(auth_url)
        params = parse_qs(parsed.query)
        print(f"   Client ID: {params.get('client_id', [''])[0][:20]}...")
        print(f"   Redirect URI: {params.get('redirect_uri', [''])[0]}")
        
    except Exception as e:
        print(f"❌ Failed to get auth URL: {e}")
        return
    
    # Step 3: Show instructions for manual testing
    print("\n3️⃣ Manual Testing Instructions:")
    print(f"   1. Open your browser and navigate to:")
    print(f"      {auth_url}")
    print(f"   2. Authorize the application with DigiKey")
    print(f"   3. You'll be redirected to: http://localhost:8000/api/template-sync/callback")
    print(f"   4. The callback will redirect you to: http://localhost:3000/?code=YOUR_CODE")
    print(f"   5. The frontend will automatically detect the code and open the auth dialog")
    
    # Step 4: Test callback endpoint format
    print("\n4️⃣ Testing callback endpoint format...")
    test_code = "test123"
    try:
        response = requests.get(f"{base_url}/api/template-sync/callback-info?code={test_code}")
        callback_data = response.json()
        print(f"   Callback response: {json.dumps(callback_data, indent=2)}")
    except Exception as e:
        print(f"❌ Failed to test callback: {e}")
    
    print("\n✅ OAuth flow endpoints are ready for testing!")
    print("🌐 Open http://localhost:3000 and click 'DigiKey Admin' in the sidebar")
    print("🔗 Then click 'Authorize with DigiKey' to start the OAuth flow")

if __name__ == "__main__":
    test_oauth_flow()