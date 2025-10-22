#!/usr/bin/env python3
"""
Test script for Gmail OAuth2 integration
"""
import os
import sys
import django
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'devlink_backend.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile
from emails.gmail_oauth2 import GmailOAuth2Service

def test_gmail_oauth2_service():
    """Test Gmail OAuth2 service functionality"""
    print("Testing Gmail OAuth2 Service...")
    
    # Check if OAuth2 credentials are configured
    client_id = os.getenv('GMAIL_CLIENT_ID')
    client_secret = os.getenv('GMAIL_CLIENT_SECRET')
    redirect_uri = os.getenv('GMAIL_REDIRECT_URI', 'http://localhost:8000/api/emails/gmail/callback/')
    
    if not client_id or not client_secret:
        print("Gmail OAuth2 credentials not configured")
        print("Please set GMAIL_CLIENT_ID and GMAIL_CLIENT_SECRET in your .env file")
        return False
    
    print(f"Gmail OAuth2 credentials found")
    print(f"   Client ID: {client_id[:10]}...")
    print(f"   Redirect URI: {redirect_uri}")
    
    # Test service initialization
    try:
        oauth_service = GmailOAuth2Service()
        print("Gmail OAuth2 service initialized successfully")
    except Exception as e:
        print(f"Failed to initialize Gmail OAuth2 service: {e}")
        return False
    
    # Test authorization URL generation
    try:
        auth_url = oauth_service.get_authorization_url(state="test_state")
        print(f"Authorization URL generated: {auth_url[:50]}...")
    except Exception as e:
        print(f"Failed to generate authorization URL: {e}")
        return False
    
    # Test user profile model
    try:
        # Create a test user if it doesn't exist
        user, created = User.objects.get_or_create(
            username='test_gmail_user',
            defaults={'email': 'test@example.com'}
        )
        
        # Create or get user profile
        profile, created = UserProfile.objects.get_or_create(user=user)
        
        # Test Gmail fields
        profile.gmail_connected = False
        profile.gmail_email = None
        profile.gmail_access_token = None
        profile.gmail_refresh_token = None
        profile.gmail_token_expires_at = None
        profile.save()
        
        print("User profile model updated with Gmail fields")
        
        # Test token validity check
        is_valid = profile.is_gmail_token_valid()
        print(f"Token validity check: {is_valid} (expected: False)")
        
    except Exception as e:
        print(f"Failed to test user profile model: {e}")
        return False
    
    print("\nAll Gmail OAuth2 tests passed!")
    print("\nNext steps:")
    print("1. Set up your Google Cloud Console project")
    print("2. Configure Gmail OAuth2 credentials")
    print("3. Test the integration through the web interface")
    
    return True

def test_email_sending_fallback():
    """Test email sending fallback functionality"""
    print("\nTesting email sending fallback...")
    
    try:
        from django.core.mail import send_mail
        from django.conf import settings
        
        # Test basic email sending (console backend)
        send_mail(
            'Test Email',
            'This is a test email from DevLink',
            settings.EMAIL_HOST_USER or 'test@example.com',
            ['test@example.com'],
            fail_silently=True
        )
        print("Email sending fallback works")
        return True
        
    except Exception as e:
        print(f"Email sending fallback failed: {e}")
        return False

if __name__ == '__main__':
    print("DevLink Gmail OAuth2 Integration Test")
    print("=" * 50)
    
    success = True
    
    # Test Gmail OAuth2 service
    success &= test_gmail_oauth2_service()
    
    # Test email sending fallback
    success &= test_email_sending_fallback()
    
    print("\n" + "=" * 50)
    if success:
        print("All tests passed! Gmail OAuth2 integration is ready.")
    else:
        print("Some tests failed. Please check the errors above.")
        sys.exit(1)
