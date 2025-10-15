#!/usr/bin/env python
"""
Test authentication flow
"""
import requests
import json

def test_auth_flow():
    base_url = 'http://127.0.0.1:8000/api'
    
    print("Testing authentication flow...")
    print("-" * 50)
    
    # Test 1: Register a test user
    print("1. Registering test user...")
    register_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass123'
    }
    
    try:
        response = requests.post(f'{base_url}/auth/register/', json=register_data)
        if response.status_code == 201:
            print("SUCCESS: User registered")
        elif response.status_code == 400 and 'already exists' in response.text:
            print("INFO: User already exists (that's fine)")
        else:
            print(f"ERROR: Registration failed - {response.status_code}: {response.text}")
    except Exception as e:
        print(f"EXCEPTION during registration: {str(e)}")
    
    # Test 2: Login
    print("\n2. Logging in...")
    login_data = {
        'username': 'testuser',
        'password': 'testpass123'
    }
    
    try:
        response = requests.post(f'{base_url}/auth/login/', json=login_data)
        if response.status_code == 200:
            data = response.json()
            token = data.get('access')
            print(f"SUCCESS: Login successful, token: {token[:20]}...")
            
            # Test 3: Get user info
            print("\n3. Getting user info...")
            headers = {'Authorization': f'Bearer {token}'}
            response = requests.get(f'{base_url}/auth/me/', headers=headers)
            if response.status_code == 200:
                user_data = response.json()
                print(f"SUCCESS: User info - {user_data}")
            else:
                print(f"ERROR: Get user info failed - {response.status_code}: {response.text}")
                
        else:
            print(f"ERROR: Login failed - {response.status_code}: {response.text}")
    except Exception as e:
        print(f"EXCEPTION during login: {str(e)}")
    
    # Test 4: Test email generation without auth (should work)
    print("\n4. Testing email generation (no auth required)...")
    email_data = {
        'business_name': 'Test Business',
        'business_category': 'restaurant',
        'developer_name': 'Test Developer',
        'developer_services': 'Web development'
    }
    
    try:
        response = requests.post(f'{base_url}/ai/generate-email/', json=email_data)
        if response.status_code == 200:
            data = response.json()
            print(f"SUCCESS: Email generated - Subject: {data.get('subject')}")
        else:
            print(f"ERROR: Email generation failed - {response.status_code}: {response.text}")
    except Exception as e:
        print(f"EXCEPTION during email generation: {str(e)}")

if __name__ == '__main__':
    test_auth_flow()
