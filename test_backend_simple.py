#!/usr/bin/env python
"""
Simple backend API tests for DevLink application
"""
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_URL = "http://127.0.0.1:8000/api"

def test_api_root():
    """Test API root endpoint"""
    print("1. Testing API root...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   SUCCESS: API root accessible")
        else:
            print("   ERROR: API root failed")
    except Exception as e:
        print(f"   ERROR: API root error: {e}")

def test_auth_endpoints():
    """Test authentication endpoints"""
    print("\n2. Testing authentication endpoints...")
    
    # Test register endpoint
    try:
        register_data = {
            "username": "testuser_api",
            "email": "testapi@example.com",
            "password": "testpass123"
        }
        response = requests.post(f"{BASE_URL}/auth/register/", json=register_data)
        print(f"   Register Status: {response.status_code}")
        if response.status_code in [200, 201, 400]:  # 400 if user already exists
            print("   SUCCESS: Register endpoint working")
        else:
            print("   ERROR: Register endpoint failed")
    except Exception as e:
        print(f"   ERROR: Register error: {e}")
    
    # Test login endpoint
    try:
        login_data = {
            "username": "testuser_api",
            "password": "testpass123"
        }
        response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
        print(f"   Login Status: {response.status_code}")
        if response.status_code == 200:
            print("   SUCCESS: Login endpoint working")
            return response.json().get('access')
        else:
            print("   ERROR: Login endpoint failed")
    except Exception as e:
        print(f"   ERROR: Login error: {e}")
    
    return None

def test_ai_endpoints():
    """Test AI service endpoints"""
    print("\n3. Testing AI service endpoints...")
    
    # Test email generation
    try:
        email_data = {
            "business_name": "Test Restaurant",
            "business_category": "restaurant",
            "developer_name": "Test Developer",
            "developer_services": "Web development"
        }
        response = requests.post(f"{BASE_URL}/ai/generate-email/", json=email_data)
        print(f"   Email Generation Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   SUCCESS: Email generated: {data.get('subject', 'No subject')[:50]}...")
        else:
            print("   ERROR: Email generation failed")
    except Exception as e:
        print(f"   ERROR: Email generation error: {e}")
    
    # Test business generation
    try:
        business_data = {
            "city": "Pisa",
            "country": "Italy",
            "category": "restaurant"
        }
        response = requests.post(f"{BASE_URL}/ai/generate-businesses/", json=business_data)
        print(f"   Business Generation Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                print(f"   SUCCESS: Found {len(data)} businesses")
            else:
                print("   WARNING: No businesses found (might be API key issue)")
        else:
            print("   ERROR: Business generation failed")
    except Exception as e:
        print(f"   ERROR: Business generation error: {e}")

def test_cors_headers():
    """Test CORS headers"""
    print("\n4. Testing CORS headers...")
    try:
        headers = {
            'Origin': 'http://localhost:3001',
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'Content-Type'
        }
        response = requests.options(f"{BASE_URL}/auth/login/", headers=headers)
        print(f"   CORS Status: {response.status_code}")
        
        cors_headers = {
            'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
            'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
            'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers')
        }
        
        if response.status_code == 200 and cors_headers['Access-Control-Allow-Origin']:
            print("   SUCCESS: CORS headers present")
            print(f"   Allowed Origins: {cors_headers['Access-Control-Allow-Origin']}")
        else:
            print("   ERROR: CORS headers missing")
    except Exception as e:
        print(f"   ERROR: CORS test error: {e}")

def test_environment_variables():
    """Test environment variable loading"""
    print("\n5. Testing environment variables...")
    
    required_vars = [
        'GEMINI_API_KEY',
        'GOOGLE_PLACES_API_KEY',
        'ALLOWED_HOSTS',
        'CORS_ALLOWED_ORIGINS'
    ]
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"   SUCCESS: {var}: {'*' * 10}...{value[-4:] if len(value) > 4 else '***'}")
        else:
            print(f"   ERROR: {var}: Not set")

def main():
    """Run all tests"""
    print("DevLink Backend API Tests")
    print("=" * 50)
    
    test_api_root()
    token = test_auth_endpoints()
    test_ai_endpoints()
    test_cors_headers()
    test_environment_variables()
    
    print("\n" + "=" * 50)
    print("SUCCESS: Backend API tests completed!")
    print("\nIf all tests show SUCCESS, your backend is working correctly.")
    print("If any show ERROR, check the Django server and .env configuration.")

if __name__ == '__main__':
    main()
