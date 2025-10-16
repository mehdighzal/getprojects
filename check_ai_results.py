#!/usr/bin/env python3
"""
Check AI Bulk Email Results
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def check_results():
    print("Checking AI Bulk Email Results")
    print("=" * 40)
    
    # Login
    login_response = requests.post(f"{BASE_URL}/auth/login/", json={
        "username": "testuser5",
        "password": "testpass123"
    })
    token = login_response.json().get("access")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Check email history
    print("\n1. Checking Email History...")
    history_response = requests.get(f"{BASE_URL}/email/history/?page=1&page_size=10", headers=headers)
    if history_response.status_code == 200:
        history = history_response.json()
        emails = history.get("results", [])
        print(f"Found {len(emails)} emails in history:")
        for i, email in enumerate(emails[:3]):
            subject = email.get("subject", "N/A")
            recipients = email.get("recipients", [])
            status = email.get("status", "N/A")
            body = email.get("body", "")
            print(f"{i+1}. Subject: {subject[:60]}...")
            print(f"   Recipients: {recipients}")
            print(f"   Status: {status}")
            print(f"   Body preview: {body[:100]}...")
            print()
    else:
        print(f"Error getting history: {history_response.status_code}")
    
    # Check campaign status
    print("\n2. Checking Campaign Status...")
    campaign_response = requests.get(f"{BASE_URL}/email/campaigns/4/", headers=headers)
    if campaign_response.status_code == 200:
        campaign = campaign_response.json()
        print(f"Campaign Status: {campaign.get('status')}")
        print(f"Sent: {campaign.get('sent_count', 0)}/{campaign.get('total_count', 0)}")
        if campaign.get('status') == 'completed':
            print("SUCCESS: Campaign completed with AI-generated emails!")
        elif campaign.get('status') == 'sending':
            print("INFO: Campaign is still sending...")
    else:
        print(f"Error getting campaign: {campaign_response.status_code}")

if __name__ == '__main__':
    check_results()
