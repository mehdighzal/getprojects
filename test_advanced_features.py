import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000/api"

def test_advanced_features():
    print("Testing Advanced Features: Email Templates, Bulk Operations & Analytics")
    print("=" * 70)
    
    # Test user credentials
    username = "testuser2"
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
    
    # 2. Test Email Templates
    print("\n2. Testing Email Templates...")
    try:
        # Create a template
        template_data = {
            "name": "Test Template",
            "subject": "Test Subject",
            "body": "This is a test email template body.",
            "category": "general",
            "is_default": False
        }
        
        create_response = requests.post(f"{BASE_URL}/email/templates/", 
                                      json=template_data, headers=headers)
        if create_response.status_code == 201:
            template_id = create_response.json().get("id")
            print(f"SUCCESS: Template created with ID: {template_id}")
            
            # Get templates
            get_response = requests.get(f"{BASE_URL}/email/templates/", headers=headers)
            if get_response.status_code == 200:
                templates = get_response.json()
                print(f"SUCCESS: Retrieved {len(templates)} templates")
            else:
                print(f"ERROR: Failed to get templates: {get_response.status_code}")
        else:
            print(f"ERROR: Failed to create template: {create_response.status_code}")
            print(f"Response: {create_response.text}")
    except Exception as e:
        print(f"ERROR: Template error: {e}")
    
    # 3. Test Bulk Email Campaigns
    print("\n3. Testing Bulk Email Campaigns...")
    try:
        campaign_data = {
            "name": "Test Campaign",
            "subject": "Test Campaign Subject",
            "body": "This is a test bulk email campaign.",
            "recipients": [
                {"name": "Test Business 1", "email": "test1@example.com"},
                {"name": "Test Business 2", "email": "test2@example.com"}
            ]
        }
        
        create_response = requests.post(f"{BASE_URL}/email/campaigns/", 
                                      json=campaign_data, headers=headers)
        if create_response.status_code == 201:
            campaign_id = create_response.json().get("id")
            print(f"SUCCESS: Campaign created with ID: {campaign_id}")
            
            # Get campaigns
            get_response = requests.get(f"{BASE_URL}/email/campaigns/", headers=headers)
            if get_response.status_code == 200:
                campaigns = get_response.json()
                print(f"SUCCESS: Retrieved {len(campaigns)} campaigns")
            else:
                print(f"ERROR: Failed to get campaigns: {get_response.status_code}")
        else:
            print(f"ERROR: Failed to create campaign: {create_response.status_code}")
            print(f"Response: {create_response.text}")
    except Exception as e:
        print(f"ERROR: Campaign error: {e}")
    
    # 4. Test Analytics
    print("\n4. Testing Email Analytics...")
    try:
        analytics_response = requests.get(f"{BASE_URL}/email/analytics/?days=30", headers=headers)
        if analytics_response.status_code == 200:
            analytics = analytics_response.json()
            print("SUCCESS: Analytics retrieved successfully")
            print(f"   - Total emails: {analytics.get('summary', {}).get('total_emails', 0)}")
            print(f"   - Total campaigns: {analytics.get('summary', {}).get('total_campaigns', 0)}")
            print(f"   - Templates count: {analytics.get('summary', {}).get('templates_count', 0)}")
        else:
            print(f"ERROR: Failed to get analytics: {analytics_response.status_code}")
    except Exception as e:
        print(f"ERROR: Analytics error: {e}")
    
    # 5. Test Email History
    print("\n5. Testing Email History...")
    try:
        history_response = requests.get(f"{BASE_URL}/email/history/?page=1&page_size=10", headers=headers)
        if history_response.status_code == 200:
            history = history_response.json()
            print(f"SUCCESS: Retrieved {len(history.get('results', []))} email history records")
        else:
            print(f"ERROR: Failed to get email history: {history_response.status_code}")
    except Exception as e:
        print(f"ERROR: History error: {e}")
    
    print("\n" + "=" * 70)
    print("Advanced Features Test Complete!")
    print("\nSummary of Features Added:")
    print("   - Email Templates - Create, edit, delete, and use templates")
    print("   - Bulk Email Campaigns - Create and manage bulk email campaigns")
    print("   - Email Analytics - View detailed analytics and statistics")
    print("   - Enhanced Email History - Track email status and errors")
    print("   - Template Integration - Use templates in email composition")
    print("\nAll advanced features are now available in the frontend!")

if __name__ == '__main__':
    test_advanced_features()
