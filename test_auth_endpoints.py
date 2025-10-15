#!/usr/bin/env python
"""
Test authentication endpoints
"""
import requests
import json

def test_auth_endpoints():
    base_url = 'http://127.0.0.1:8000/api/auth'
    
    print("Testing authentication endpoints...")
    print("-" * 50)
    
    # Test 1: Register endpoint
    print("1. Testing register endpoint...")
    register_data = {
        'username': 'testuser2',
        'email': 'test2@example.com',
        'password': 'testpass123'
    }
    
    try:
        response = requests.post(f'{base_url}/register/', json=register_data)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 201:
            print("SUCCESS: User registered")
            data = response.json()
            print(f"Access token: {data.get('access', '')[:20]}...")
        elif response.status_code == 400:
            print(f"INFO: {response.json()}")
        else:
            print(f"ERROR: {response.text}")
    except Exception as e:
        print(f"EXCEPTION: {str(e)}")
    
    # Test 2: Login endpoint
    print("\n2. Testing login endpoint...")
    login_data = {
        'username': 'testuser2',
        'password': 'testpass123'
    }
    
    try:
        response = requests.post(f'{base_url}/login/', json=login_data)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("SUCCESS: User logged in")
            data = response.json()
            print(f"Access token: {data.get('access', '')[:20]}...")
            token = data.get('access')
        else:
            print(f"ERROR: {response.text}")
            token = None
    except Exception as e:
        print(f"EXCEPTION: {str(e)}")
        token = None
    
    # Test 3: Me endpoint
    if token:
        print("\n3. Testing me endpoint...")
        headers = {'Authorization': f'Bearer {token}'}
        try:
            response = requests.get(f'{base_url}/me/', headers=headers)
            print(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                print("SUCCESS: User info retrieved")
                data = response.json()
                print(f"User: {data.get('username')} ({data.get('email')})")
            else:
                print(f"ERROR: {response.text}")
        except Exception as e:
            print(f"EXCEPTION: {str(e)}")
    
    # Test 4: Profile endpoint
    if token:
        print("\n4. Testing profile endpoint...")
        headers = {'Authorization': f'Bearer {token}'}
        try:
            response = requests.get(f'{base_url}/profile/', headers=headers)
            print(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                print("SUCCESS: Profile retrieved")
                data = response.json()
                print(f"Profile: {data.get('username')} ({data.get('email')})")
            else:
                print(f"ERROR: {response.text}")
        except Exception as e:
            print(f"EXCEPTION: {str(e)}")

if __name__ == '__main__':
    test_auth_endpoints()
