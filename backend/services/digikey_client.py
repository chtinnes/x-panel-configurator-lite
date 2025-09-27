"""
DigiKey API Client
Handles authentication, rate limiting, and API requests to DigiKey
"""

import os
import time
import re
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
import json

# Import requests with fallback for development
try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    # Mock classes for development without requests
    class HTTPAdapter:
        def __init__(self, max_retries=None): pass
    class Retry:
        def __init__(self, total=3, backoff_factor=1, status_forcelist=None): pass
    class requests:
        class Session:
            def mount(self, prefix, adapter): pass
            def post(self, url, data=None, headers=None): pass
            def request(self, method, url, headers=None, **kwargs): pass
        class RequestException(Exception): pass

from .digikey_config import (
    DIGIKEY_SANDBOX_URL, DIGIKEY_AUTH_URL, API_VERSION, PRODUCT_INFO_VERSION,
    DEFAULT_HEADERS, RATE_LIMIT_PER_MINUTE, RATE_LIMIT_PER_DAY,
    ELECTRICAL_CATEGORIES, CURRENT_RATING_PATTERNS, VOLTAGE_RATING_PATTERNS, POLE_COUNT_PATTERNS
)

logger = logging.getLogger(__name__)


class DigiKeyRateLimiter:
    """Rate limiting for DigiKey API calls"""
    
    def __init__(self, requests_per_minute: int = RATE_LIMIT_PER_MINUTE, requests_per_day: int = RATE_LIMIT_PER_DAY):
        self.requests_per_minute = requests_per_minute
        self.requests_per_day = requests_per_day
        self.minute_requests = []
        self.daily_requests = 0
        self.daily_reset_time = datetime.now() + timedelta(days=1)
    
    def can_make_request(self) -> bool:
        """Check if we can make a request within rate limits"""
        now = datetime.now()
        
        # Reset daily counter if needed
        if now > self.daily_reset_time:
            self.daily_requests = 0
            self.daily_reset_time = now + timedelta(days=1)
        
        # Clean old minute requests
        cutoff = now - timedelta(minutes=1)
        self.minute_requests = [req_time for req_time in self.minute_requests if req_time > cutoff]
        
        # Check limits
        minute_ok = len(self.minute_requests) < self.requests_per_minute
        daily_ok = self.daily_requests < self.requests_per_day
        
        return minute_ok and daily_ok
    
    def record_request(self):
        """Record that a request was made"""
        self.minute_requests.append(datetime.now())
        self.daily_requests += 1
    
    def wait_time(self) -> int:
        """Get seconds to wait before next request"""
        if not self.minute_requests:
            return 0
        
        oldest_request = min(self.minute_requests)
        wait_until = oldest_request + timedelta(minutes=1)
        wait_seconds = max(0, (wait_until - datetime.now()).total_seconds())
        return int(wait_seconds) + 1


class DigiKeyAPIClient:
    """DigiKey API Client with OAuth 2.0 authentication and rate limiting"""
    
    def __init__(self, client_id: Optional[str] = None, client_secret: Optional[str] = None, use_sandbox: bool = True):
        self.client_id = client_id or os.getenv('DIGIKEY_CLIENT_ID')
        self.client_secret = client_secret or os.getenv('DIGIKEY_CLIENT_SECRET')
        self.use_sandbox = use_sandbox
        self.base_url = DIGIKEY_SANDBOX_URL if use_sandbox else "https://api.digikey.com"
        
        self.access_token = None
        self.token_expires_at = None
        self.rate_limiter = DigiKeyRateLimiter()
        
        # Setup session with retries
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
    
    def is_configured(self) -> bool:
        """Check if API credentials are configured"""
        return bool(self.client_id and self.client_secret)
    
    def get_oauth_url(self) -> str:
        """Get OAuth authorization URL for manual authentication"""
        if not self.is_configured():
            raise ValueError("DigiKey API credentials not configured")
        
        # Use sandbox or production URL based on mode
        auth_base_url = self.base_url  # This will be sandbox-api.digikey.com or api.digikey.com
        
        # DigiKey OAuth 2.0 uses the v1/oauth2/authorize endpoint
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': 'https://localhost:3000/template-sync/callback',  # Frontend callback route
        }
        
        from urllib.parse import urlencode
        query_string = urlencode(params)
        auth_url = f"{auth_base_url}/v1/oauth2/authorize?{query_string}"
        
        logger.info(f"Generated OAuth URL for {'sandbox' if self.use_sandbox else 'production'}: {auth_url}")
        return auth_url
    
    def authenticate_with_code(self, authorization_code: str) -> bool:
        """Exchange authorization code for access token"""
        if not self.is_configured():
            logger.error("DigiKey API credentials not configured")
            return False
        
        token_data = {
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': 'https://localhost:3000/template-sync/callback'  # Must match authorization request
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/v1/oauth2/token",
                data=token_data,
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )
            response.raise_for_status()
            
            token_response = response.json()
            self.access_token = token_response.get('access_token')
            expires_in = token_response.get('expires_in', 3600)
            self.token_expires_at = datetime.now() + timedelta(seconds=expires_in)
            
            logger.info("Successfully authenticated with DigiKey API")
            return True
            
        except requests.RequestException as e:
            logger.error(f"Failed to authenticate with DigiKey API: {e}")
            return False
    
    def _wait_for_rate_limit(self):
        """Wait if necessary to respect rate limits"""
        if not self.rate_limiter.can_make_request():
            wait_time = self.rate_limiter.wait_time()
            if wait_time > 0:
                logger.info(f"Rate limit reached, waiting {wait_time} seconds...")
                time.sleep(wait_time)
    
    def _make_api_request(self, method: str, endpoint: str, **kwargs) -> Optional[Dict]:
        """Make authenticated API request with rate limiting"""
        if not self.access_token:
            logger.error("No access token available. Please authenticate first.")
            return None
        
        self._wait_for_rate_limit()
        
        headers = DEFAULT_HEADERS.copy()
        headers['Authorization'] = f'Bearer {self.access_token}'
        
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = self.session.request(method, url, headers=headers, **kwargs)
            self.rate_limiter.record_request()
            
            if response.status_code == 429:
                logger.warning("Rate limit exceeded, will retry...")
                retry_after = int(response.headers.get('Retry-After', 60))
                time.sleep(retry_after)
                return self._make_api_request(method, endpoint, **kwargs)
            
            response.raise_for_status()
            return response.json()
            
        except requests.RequestException as e:
            logger.error(f"API request failed: {e}")
            return None
    
    def search_products(self, keyword: str, manufacturer: Optional[str] = None, category: Optional[str] = None, limit: int = 50) -> Optional[List[Dict]]:
        """Search for products using DigiKey Product Information API v4"""
        search_data = {
            "Keywords": keyword,
            "RecordCount": limit,
            "RecordStartPosition": 0,
            "Filters": {}
        }
        
        # Add manufacturer filter if specified
        if manufacturer:
            search_data["Filters"]["Manufacturer"] = [manufacturer]
        
        # Add category filter if specified  
        if category:
            search_data["Filters"]["CategoryName"] = [category]
        
        endpoint = f"Search/{PRODUCT_INFO_VERSION}/Products/Keyword"
        response = self._make_api_request("POST", endpoint, json=search_data)
        
        if response and "Products" in response:
            logger.info(f"Found {len(response['Products'])} products for '{keyword}'")
            return response["Products"]
        
        return []
    
    def get_product_details(self, part_number: str) -> Optional[Dict]:
        """Get detailed information for a specific part number"""
        endpoint = f"Search/{PRODUCT_INFO_VERSION}/Products/{part_number}"
        response = self._make_api_request("GET", endpoint)
        
        if response and "Product" in response:
            return response["Product"]
        
        return None
    
    def search_electrical_components(self, component_type: str, manufacturer: str = "Hager", limit: int = 50) -> List[Dict]:
        """Search for specific electrical components"""
        if component_type not in ELECTRICAL_CATEGORIES:
            logger.error(f"Unknown component type: {component_type}")
            return []
        
        category_config = ELECTRICAL_CATEGORIES[component_type]
        search_terms = category_config["search_terms"]
        
        all_products = []
        
        for search_term in search_terms:
            products = self.search_products(
                keyword=f"{manufacturer} {search_term}",
                manufacturer=manufacturer,
                limit=limit
            )
            
            if products:
                all_products.extend(products)
                # Stop after finding products to avoid duplicate results
                break
        
        # Remove duplicates based on part number
        unique_products = {}
        for product in all_products:
            part_number = product.get("DigiKeyPartNumber")
            if part_number and part_number not in unique_products:
                unique_products[part_number] = product
        
        return list(unique_products.values())[:limit]
    
    def extract_specifications(self, product: Dict) -> Dict[str, Any]:
        """Extract electrical specifications from DigiKey product data"""
        specs = {}
        
        # Get basic product info
        specs["part_number"] = product.get("DigiKeyPartNumber", "")
        specs["manufacturer"] = product.get("Manufacturer", {}).get("Name", "")
        specs["description"] = product.get("ProductDescription", "")
        specs["category"] = product.get("Category", {}).get("Name", "")
        
        # Extract technical parameters from product description and parameters
        description = specs["description"].upper()
        
        # Extract current rating
        for pattern in CURRENT_RATING_PATTERNS:
            match = re.search(pattern, description)
            if match:
                specs["current_rating"] = int(match.group(1))
                break
        
        # Extract voltage rating  
        for pattern in VOLTAGE_RATING_PATTERNS:
            match = re.search(pattern, description)
            if match:
                specs["voltage_rating"] = int(match.group(1))
                break
        
        # Extract pole count
        for pattern in POLE_COUNT_PATTERNS:
            match = re.search(pattern, description)
            if match:
                specs["pole_count"] = int(match.group(1))
                break
        
        # Extract from Parameters array if available
        parameters = product.get("Parameters", [])
        for param in parameters:
            param_name = param.get("Parameter", "").lower()
            param_value = param.get("Value", "")
            
            if "current" in param_name and "rating" in param_name:
                # Extract numeric value from parameter
                current_match = re.search(r"(\d+)", param_value)
                if current_match:
                    specs["current_rating"] = int(current_match.group(1))
            
            elif "voltage" in param_name:
                voltage_match = re.search(r"(\d+)", param_value)
                if voltage_match:
                    specs["voltage_rating"] = int(voltage_match.group(1))
            
            elif "pole" in param_name or "way" in param_name:
                pole_match = re.search(r"(\d+)", param_value)
                if pole_match:
                    specs["pole_count"] = int(pole_match.group(1))
        
        # Add pricing info if available
        pricing = product.get("StandardPricing", [])
        if pricing:
            specs["unit_price"] = pricing[0].get("UnitPrice", 0.0)
            specs["currency"] = pricing[0].get("CurrencyCode", "USD")
        
        # Add availability
        specs["quantity_available"] = product.get("QuantityAvailable", 0)
        
        return specs