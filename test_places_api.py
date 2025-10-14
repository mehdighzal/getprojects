#!/usr/bin/env python
"""
Test script for Google Places API integration
"""
import requests
import json

def test_places_api():
    url = 'http://127.0.0.1:8000/api/ai/generate-businesses/'
    
    # Test query: restaurants in Pisa, Italy
    payload = {
        'city': 'Pisa',
        'country': 'Italy',
        'category': 'restaurant',
        'search': ''
    }
    
    print("Testing Google Places API integration...")
    print(f"Query: {payload}")
    print("-" * 50)
    
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                print(f"\nSUCCESS! Found {len(data)} real businesses:")
                print("-" * 50)
                
                # Display first 3 businesses
                for i, business in enumerate(data[:3], 1):
                    print(f"\n{i}. {business.get('name')}")
                    print(f"   Address: {business.get('address')}")
                    print(f"   Phone: {business.get('phone', 'N/A')}")
                    print(f"   Email: {business.get('email', 'N/A')}")
                    print(f"   Website: {business.get('website', 'N/A')}")
                    if 'rating' in business:
                        print(f"   Rating: {business.get('rating')} stars ({business.get('user_ratings_total', 0)} reviews)")
                
                print(f"\n... and {len(data) - 3} more businesses" if len(data) > 3 else "")
            else:
                print(f"\nWARNING Response: {data}")
        else:
            print(f"\nERROR: {response.text}")
    
    except Exception as e:
        print(f"\nEXCEPTION ERROR: {str(e)}")

if __name__ == '__main__':
    test_places_api()

