#!/usr/bin/env python
"""
Test frontend-backend connection
"""
import requests
import json

def test_frontend_connection():
    print("Testing frontend-backend connection...")
    print("-" * 50)
    
    # Test 1: Check if backend is accessible
    print("1. Testing backend accessibility...")
    try:
        response = requests.get('http://127.0.0.1:8000/api/auth/me/', timeout=5)
        print(f"Backend Status: {response.status_code}")
        if response.status_code == 401:
            print("SUCCESS: Backend is accessible (401 is expected without auth)")
        else:
            print(f"Backend response: {response.text[:100]}")
    except Exception as e:
        print(f"ERROR: Backend not accessible: {str(e)}")
        return
    
    # Test 2: Test CORS preflight
    print("\n2. Testing CORS preflight...")
    try:
        headers = {
            'Origin': 'http://0.0.0.0:3001',
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'Content-Type,Authorization'
        }
        response = requests.options('http://127.0.0.1:8000/api/auth/login/', headers=headers, timeout=5)
        print(f"CORS Status: {response.status_code}")
        cors_headers = {
            'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
            'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
            'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers')
        }
        print(f"CORS Headers: {cors_headers}")
        if response.status_code == 200:
            print("SUCCESS: CORS preflight successful")
        else:
            print("ERROR: CORS preflight failed")
    except Exception as e:
        print(f"ERROR: CORS test failed: {str(e)}")
    
    # Test 3: Test actual login request with CORS
    print("\n3. Testing login with CORS headers...")
    try:
        headers = {
            'Origin': 'http://0.0.0.0:3001',
            'Content-Type': 'application/json'
        }
        data = {
            'username': 'testuser2',
            'password': 'testpass123'
        }
        response = requests.post('http://127.0.0.1:8000/api/auth/login/', 
                               json=data, headers=headers, timeout=5)
        print(f"Login Status: {response.status_code}")
        if response.status_code == 200:
            print("SUCCESS: Login successful with CORS")
            data = response.json()
            print(f"Token: {data.get('access', '')[:20]}...")
        else:
            print(f"ERROR: Login failed: {response.text}")
    except Exception as e:
        print(f"ERROR: Login test failed: {str(e)}")

if __name__ == '__main__':
    test_frontend_connection()
