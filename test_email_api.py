#!/usr/bin/env python
"""
Test email generation API endpoint
"""
import requests
import json

def test_email_generation():
    url = 'http://127.0.0.1:8000/api/ai/generate-email/'
    
    payload = {
        'business_name': 'Test Restaurant',
        'business_category': 'restaurant',
        'developer_name': 'John Developer',
        'developer_services': 'Web development and digital solutions'
    }
    
    print("Testing email generation API...")
    print(f"Payload: {payload}")
    print("-" * 50)
    
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("SUCCESS! Email generated:")
            print(f"Subject: {data.get('subject')}")
            print(f"Body: {data.get('body')[:100]}...")
            print(f"Source: {data.get('source')}")
        else:
            print(f"ERROR: {response.text}")
    
    except Exception as e:
        print(f"EXCEPTION: {str(e)}")

if __name__ == '__main__':
    test_email_generation()
