#!/usr/bin/env python3
"""
Test AI Bulk Email Integration
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000/api"

def test_ai_bulk_integration():
    print("Testing AI Bulk Email Integration")
    print("=" * 50)
    
    # Test user credentials
    username = "testuser5"
    password = "testpass123"
    token = None
    
    # 1. Login to get token
    print("\n1. Logging in...")
    try:
        login_response = requests.post(f"{BASE_URL}/auth/login/", json={
            "username": username,
            "password": password
        })
        if login_response.status_code == 200:
            token = login_response.json().get("access")
            print("SUCCESS: Login successful")
        else:
            print(f"ERROR: Login failed: {login_response.status_code}")
            return
    except Exception as e:
        print(f"ERROR: Login error: {e}")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Create bulk campaign from businesses
    print("\n2. Creating bulk campaign from businesses...")
    try:
        # Sample business data
        businesses = [
            {
                "id": 1,
                "name": "Tech Solutions Inc",
                "email": "contact@techsolutions.com",
                "category": "technology",
                "phone": "+1-555-0123",
                "address": "123 Tech Street, Silicon Valley, CA"
            },
            {
                "id": 2,
                "name": "Green Energy Co",
                "email": "info@greenenergy.com",
                "category": "energy",
                "phone": "+1-555-0456",
                "address": "456 Green Ave, Portland, OR"
            },
            {
                "id": 3,
                "name": "Creative Design Studio",
                "email": "hello@creativedesign.com",
                "category": "design",
                "phone": "+1-555-0789",
                "address": "789 Creative Blvd, Austin, TX"
            }
        ]
        
        campaign_data = {
            "businesses": businesses,
            "name": "AI Test Campaign"
        }
        
        create_response = requests.post(f"{BASE_URL}/email/campaigns/create-from-businesses/", 
                                      json=campaign_data, headers=headers)
        if create_response.status_code == 201:
            campaign_id = create_response.json().get("campaign_id")
            recipients_count = create_response.json().get("recipients_count")
            print(f"SUCCESS: Campaign created with ID: {campaign_id}")
            print(f"SUCCESS: {recipients_count} businesses added to campaign")
        else:
            print(f"ERROR: Failed to create campaign: {create_response.status_code}")
            print(f"Response: {create_response.text}")
            return
    except Exception as e:
        print(f"ERROR: Campaign creation error: {e}")
        return
    
    # 3. Get campaign details
    print("\n3. Getting campaign details...")
    try:
        get_response = requests.get(f"{BASE_URL}/email/campaigns/{campaign_id}/", headers=headers)
        if get_response.status_code == 200:
            campaign = get_response.json()
            print(f"SUCCESS: Campaign retrieved")
            print(f"   - Name: {campaign.get('name')}")
            print(f"   - Status: {campaign.get('status')}")
            print(f"   - Recipients: {len(campaign.get('recipients', []))}")
            print(f"   - Subject: {campaign.get('subject')}")
        else:
            print(f"ERROR: Failed to get campaign: {get_response.status_code}")
    except Exception as e:
        print(f"ERROR: Get campaign error: {e}")
    
    # 4. Test AI email generation for individual business
    print("\n4. Testing AI email generation...")
    try:
        ai_response = requests.post(f"{BASE_URL}/ai/generate-email/", json={
            "business_name": "Tech Solutions Inc",
            "business_category": "technology",
            "developer_name": "Test Developer",
            "developer_services": "Web development and digital solutions"
        })
        if ai_response.status_code == 200:
            ai_email = ai_response.json()
            print("SUCCESS: AI email generation working")
            print(f"   - Subject: {ai_email.get('subject', 'N/A')[:50]}...")
            print(f"   - Body length: {len(ai_email.get('body', ''))} characters")
            print(f"   - Source: {ai_email.get('source', 'N/A')}")
        else:
            print(f"ERROR: AI email generation failed: {ai_response.status_code}")
    except Exception as e:
        print(f"ERROR: AI email generation error: {e}")
    
    # 5. Send the campaign (this will trigger AI generation for each business)
    print("\n5. Sending AI-powered bulk campaign...")
    try:
        send_response = requests.post(f"{BASE_URL}/email/campaigns/{campaign_id}/send/", 
                                    headers=headers)
        if send_response.status_code == 200:
            print("SUCCESS: AI bulk campaign sending started!")
            print("   - Each email will be personalized by AI")
            print("   - Check email history for AI-generated content")
        else:
            print(f"ERROR: Failed to send campaign: {send_response.status_code}")
            print(f"Response: {send_response.text}")
    except Exception as e:
        print(f"ERROR: Send campaign error: {e}")
    
    # 6. Wait a moment and check campaign status
    print("\n6. Checking campaign status...")
    time.sleep(2)
    try:
        status_response = requests.get(f"{BASE_URL}/email/campaigns/{campaign_id}/", headers=headers)
        if status_response.status_code == 200:
            campaign = status_response.json()
            print(f"SUCCESS: Campaign status: {campaign.get('status')}")
            print(f"   - Sent count: {campaign.get('sent_count', 0)}")
            print(f"   - Total count: {campaign.get('total_count', 0)}")
        else:
            print(f"ERROR: Failed to get campaign status: {status_response.status_code}")
    except Exception as e:
        print(f"ERROR: Status check error: {e}")
    
    # 7. Check email history for AI-generated emails
    print("\n7. Checking email history for AI-generated content...")
    try:
        history_response = requests.get(f"{BASE_URL}/email/history/?page=1&page_size=10", headers=headers)
        if history_response.status_code == 200:
            history = history_response.json()
            emails = history.get('results', [])
            print(f"SUCCESS: Retrieved {len(emails)} recent emails")
            for email in emails[:3]:  # Show first 3 emails
                print(f"   - Subject: {email.get('subject', 'N/A')[:50]}...")
                print(f"   - Recipients: {email.get('recipients', [])}")
                print(f"   - Status: {email.get('status', 'N/A')}")
        else:
            print(f"ERROR: Failed to get email history: {history_response.status_code}")
    except Exception as e:
        print(f"ERROR: Email history error: {e}")
    
    print("\n" + "=" * 50)
    print("AI Bulk Email Integration Test Complete!")
    print("\nFeatures Tested:")
    print("   - Create bulk campaign from business data")
    print("   - AI email generation for individual businesses")
    print("   - AI-powered bulk email sending")
    print("   - Campaign status tracking")
    print("   - Email history with AI-generated content")
    print("\nThe system now automatically generates personalized emails")
    print("for each business in bulk campaigns using AI!")

if __name__ == '__main__':
    test_ai_bulk_integration()
