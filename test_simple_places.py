#!/usr/bin/env python
"""
Simple test to check Google Places API directly
"""
import os
import googlemaps
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_google_places_directly():
    api_key = os.getenv('GOOGLE_PLACES_API_KEY', '')
    print(f"API Key: {api_key[:20]}..." if api_key else "No API key found")
    
    if not api_key:
        print("ERROR: No API key found in .env")
        return
    
    try:
        # Initialize client
        gmaps = googlemaps.Client(key=api_key)
        print("SUCCESS: Google Maps client initialized")
        
        # Test 1: Simple geocoding
        print("\n1. Testing geocoding...")
        geocode_result = gmaps.geocode("Pisa, Italy")
        if geocode_result:
            location = geocode_result[0]['geometry']['location']
            print(f"SUCCESS: Pisa coordinates: {location}")
            
            # Test 2: Places nearby search
            print("\n2. Testing places nearby search...")
            places_result = gmaps.places_nearby(
                location=location,
                radius=5000,
                type='restaurant'
            )
            
            if places_result.get('results'):
                print(f"SUCCESS: Found {len(places_result['results'])} restaurants!")
                for i, place in enumerate(places_result['results'][:3], 1):
                    print(f"   {i}. {place.get('name')} - {place.get('vicinity')}")
            else:
                print("ERROR: No restaurants found")
                
        else:
            print("ERROR: Geocoding failed")
            
        # Test 3: Text search
        print("\n3. Testing text search...")
        text_result = gmaps.places("restaurant in Pisa, Italy")
        if text_result.get('results'):
            print(f"SUCCESS: Text search found {len(text_result['results'])} results!")
            for i, place in enumerate(text_result['results'][:3], 1):
                print(f"   {i}. {place.get('name')} - {place.get('formatted_address')}")
        else:
            print("ERROR: Text search failed")
            
    except Exception as e:
        print(f"ERROR: {str(e)}")
        if "API key" in str(e):
            print("   → Check if API key is valid")
        if "billing" in str(e).lower():
            print("   → Check if billing is enabled")
        if "quota" in str(e).lower():
            print("   → Check API quotas")

if __name__ == '__main__':
    test_google_places_directly()
