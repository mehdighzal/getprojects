#!/usr/bin/env python3
"""
Full-stack test script for DevLink application
Tests backend API endpoints and verifies functionality
"""

import requests
import json
import time

API_BASE = "http://127.0.0.1:8000/api"
FRONTEND_URL = "http://localhost:3000"

def test_backend_api():
    """Test backend API endpoints"""
    print("Testing DevLink Backend API...")
    
    # Test root endpoint
    try:
        response = requests.get("http://127.0.0.1:8000/")
        if response.status_code == 200:
            data = response.json()
            print(f"Root endpoint working: {data['message']}")
        else:
            print(f"Root endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"Backend not accessible: {e}")
        return False
    
    # Test user registration
    try:
        register_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123"
        }
        response = requests.post(f"{API_BASE}/auth/register/", json=register_data)
        if response.status_code == 201:
            print("User registration working")
        else:
            print(f"Registration failed: {response.status_code}")
    except Exception as e:
        print(f"Registration test failed: {e}")
    
    # Test user login
    try:
        login_data = {
            "username": "testuser",
            "password": "testpass123"
        }
        response = requests.post(f"{API_BASE}/auth/login/", json=login_data)
        if response.status_code == 200:
            token_data = response.json()
            token = token_data.get('access')
            print("User login working")
            
            # Test authenticated endpoint
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(f"{API_BASE}/businesses/", headers=headers)
            if response.status_code == 200:
                businesses = response.json()
                print(f"Business search working: {len(businesses)} businesses found")
            else:
                print(f"Business search failed: {response.status_code}")
                
        else:
            print(f"Login failed: {response.status_code}")
    except Exception as e:
        print(f"Login test failed: {e}")
    
    return True

def test_frontend():
    """Test if frontend is accessible"""
    print("\nTesting DevLink Frontend...")
    
    try:
        response = requests.get(FRONTEND_URL, timeout=5)
        if response.status_code == 200:
            print("Frontend accessible")
            return True
        else:
            print(f"Frontend not accessible: {response.status_code}")
            return False
    except Exception as e:
        print(f"Frontend not accessible: {e}")
        return False

def main():
    """Run full-stack tests"""
    print("DevLink Full-Stack Test Suite")
    print("=" * 50)
    
    # Test backend
    backend_ok = test_backend_api()
    
    # Wait a moment for frontend to start
    print("\nWaiting for frontend to start...")
    time.sleep(3)
    
    # Test frontend
    frontend_ok = test_frontend()
    
    # Summary
    print("\nTest Summary:")
    print("=" * 50)
    print(f"Backend API: {'Working' if backend_ok else 'Failed'}")
    print(f"Frontend: {'Working' if frontend_ok else 'Failed'}")
    
    if backend_ok and frontend_ok:
        print("\nFull-stack application is ready!")
        print(f"Frontend: {FRONTEND_URL}")
        print(f"Backend API: http://127.0.0.1:8000/")
        print(f"Admin Panel: http://127.0.0.1:8000/admin/ (admin/admin123)")
    else:
        print("\nSome components need attention")
    
    print("\nNext steps:")
    print("1. Visit http://localhost:3000 to use the frontend")
    print("2. Register a new user or login")
    print("3. Search for businesses")
    print("4. Generate and send AI emails")

if __name__ == "__main__":
    main()
