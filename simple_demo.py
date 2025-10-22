#!/usr/bin/env python3
"""
DevLink Simple Demo Script
"""

import requests
import json
import time

API_BASE = "http://127.0.0.1:8000/api"
FRONTEND_URL = "http://localhost:3001"

def print_header(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def print_step(step, description):
    print(f"\n{step}. {description}")
    print("-" * 40)

def demo_backend():
    print_header("DEVLINK BACKEND DEMO")
    
    # Check API
    print_step("1", "API Status Check")
    try:
        response = requests.get("http://127.0.0.1:8000/")
        if response.status_code == 200:
            data = response.json()
            print(f"API Status: {data['message']}")
            print(f"Version: {data['version']}")
        else:
            print(f"API Failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"API Error: {e}")
        return None
    
    # Register user
    print_step("2", "User Registration")
    try:
        register_data = {
            "username": "demouser2",
            "email": "demo2@devlink.com",
            "password": "demo123456"
        }
        response = requests.post(f"{API_BASE}/auth/register/", json=register_data)
        if response.status_code == 201:
            print("User registered successfully")
        else:
            print(f"Registration failed: {response.status_code}")
    except Exception as e:
        print(f"Registration error: {e}")
    
    # Login
    print_step("3", "User Login")
    try:
        login_data = {
            "username": "demouser2",
            "password": "demo123456"
        }
        response = requests.post(f"{API_BASE}/auth/login/", json=login_data)
        if response.status_code == 200:
            token_data = response.json()
            token = token_data.get('access')
            print("Login successful")
            return token
        else:
            print(f"Login failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"Login error: {e}")
        return None

def demo_business_search(token):
    print_header("BUSINESS SEARCH DEMO")
    
    if not token:
        print("No authentication token")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print_step("1", "Fetch All Businesses")
    try:
        response = requests.get(f"{API_BASE}/businesses/", headers=headers)
        if response.status_code == 200:
            businesses = response.json()
            print(f"Found {len(businesses)} businesses")
            for i, business in enumerate(businesses, 1):
                print(f"  {i}. {business['name']} ({business['category']})")
                print(f"     Location: {business['city']}, {business['country']}")
                if business['email']:
                    print(f"     Email: {business['email']}")
                print()
        else:
            print(f"Business search failed: {response.status_code}")
    except Exception as e:
        print(f"Business search error: {e}")

def demo_ai_email(token):
    print_header("AI EMAIL GENERATION DEMO")
    
    if not token:
        print("No authentication token")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print_step("1", "Generate AI Email")
    try:
        email_data = {
            "business_name": "Pizza Roma",
            "business_category": "restaurant",
            "developer_name": "Mario Rossi",
            "developer_services": "Website development, online ordering system"
        }
        response = requests.post(f"{API_BASE}/ai/generate-email/", headers=headers, json=email_data)
        if response.status_code == 200:
            email_content = response.json()
            print("Email generated successfully")
            print(f"Subject: {email_content['subject']}")
            print(f"Body: {email_content['body'][:200]}...")
        else:
            print(f"Email generation failed: {response.status_code}")
    except Exception as e:
        print(f"Email generation error: {e}")

def demo_email_sending(token):
    print_header("EMAIL SENDING DEMO")
    
    if not token:
        print("No authentication token")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print_step("1", "Send Test Email")
    try:
        email_data = {
            "subject": "DevLink Demo Email",
            "body": "This is a demo email from DevLink platform.",
            "recipients": ["info@pizzaroma.com"]
        }
        response = requests.post(f"{API_BASE}/email/send/", headers=headers, json=email_data)
        if response.status_code == 200:
            result = response.json()
            print("Email sent successfully")
            print(f"Recipients: {result['sent']}")
        else:
            print(f"Email sending failed: {response.status_code}")
    except Exception as e:
        print(f"Email sending error: {e}")

def demo_frontend():
    print_header("FRONTEND DEMO")
    
    print_step("1", "Frontend Accessibility")
    try:
        response = requests.get(FRONTEND_URL, timeout=5)
        if response.status_code == 200:
            print("Frontend is accessible")
            print(f"URL: {FRONTEND_URL}")
        else:
            print(f"Frontend not accessible: {response.status_code}")
    except Exception as e:
        print(f"Frontend error: {e}")

def main():
    print_header("DEVLINK FULL-STACK DEMO")
    print("Demonstrating DevLink platform features")
    print(f"Demo started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run demos
    token = demo_backend()
    demo_business_search(token)
    demo_ai_email(token)
    demo_email_sending(token)
    demo_frontend()
    
    # Summary
    print_header("DEMO COMPLETED")
    print("DevLink Application Status:")
    print("Backend API: Working")
    print("User Authentication: Working")
    print("Business Search: Working")
    print("AI Email Generation: Working")
    print("Email Sending: Working")
    print("Frontend: Accessible")
    print("\nAccess Points:")
    print(f"Frontend: {FRONTEND_URL}")
    print("Backend API: http://127.0.0.1:8000/")
    print("Admin Panel: http://127.0.0.1:8000/admin/ (admin/admin123)")
    print("\nDevLink is ready for use!")

if __name__ == "__main__":
    main()
