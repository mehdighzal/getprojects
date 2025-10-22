"""
Gmail OAuth2 Service for handling Gmail authentication and email sending
"""
import os
import json
import base64
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from django.conf import settings
from django.utils import timezone
from accounts.models import UserProfile


class GmailOAuth2Service:
    """Service for handling Gmail OAuth2 authentication and email sending"""
    
    # Gmail OAuth2 endpoints
    AUTHORIZATION_URL = 'https://accounts.google.com/o/oauth2/v2/auth'
    TOKEN_URL = 'https://oauth2.googleapis.com/token'
    REVOKE_URL = 'https://oauth2.googleapis.com/revoke'
    
    # Gmail API scopes
    SCOPES = [
        'https://www.googleapis.com/auth/gmail.send',
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile'
    ]
    
    def __init__(self):
        self.client_id = os.getenv('GMAIL_CLIENT_ID')
        self.client_secret = os.getenv('GMAIL_CLIENT_SECRET')
        self.redirect_uri = os.getenv('GMAIL_REDIRECT_URI', 'http://localhost:8000/api/emails/gmail/callback/')
    
    def get_authorization_url(self, state=None):
        """Generate Gmail OAuth2 authorization URL"""
        if not self.client_id:
            raise ValueError("GMAIL_CLIENT_ID not configured. Please set GMAIL_CLIENT_ID in your environment variables.")
        
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': ' '.join(self.SCOPES),
            'response_type': 'code',
            'access_type': 'offline',
            'prompt': 'consent'
        }
        
        if state:
            params['state'] = state
        
        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        return f"{self.AUTHORIZATION_URL}?{query_string}"
    
    def exchange_code_for_tokens(self, code):
        """Exchange authorization code for access and refresh tokens"""
        if not self.client_id or not self.client_secret:
            raise ValueError("Gmail OAuth2 credentials not configured")
        
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': self.redirect_uri
        }
        
        response = requests.post(self.TOKEN_URL, data=data)
        response.raise_for_status()
        
        return response.json()
    
    def refresh_access_token(self, refresh_token):
        """Refresh expired access token using refresh token"""
        if not self.client_id or not self.client_secret:
            raise ValueError("Gmail OAuth2 credentials not configured")
        
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token'
        }
        
        response = requests.post(self.TOKEN_URL, data=data)
        response.raise_for_status()
        
        return response.json()
    
    def get_user_info(self, access_token):
        """Get user information from Gmail API"""
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', headers=headers)
        response.raise_for_status()
        return response.json()
    
    def save_tokens_to_profile(self, user, token_data, user_info=None):
        """Save OAuth2 tokens to user profile"""
        profile, created = UserProfile.objects.get_or_create(user=user)
        
        # Calculate token expiration time
        expires_in = token_data.get('expires_in', 3600)
        expires_at = timezone.now() + timedelta(seconds=expires_in)
        
        # Save tokens
        profile.gmail_access_token = token_data.get('access_token')
        profile.gmail_refresh_token = token_data.get('refresh_token')
        profile.gmail_token_expires_at = expires_at
        profile.gmail_connected = True
        
        # Save user email if available
        if user_info:
            profile.gmail_email = user_info.get('email')
        
        profile.save()
        return profile
    
    def get_valid_access_token(self, user):
        """Get valid access token, refreshing if necessary"""
        try:
            profile = user.profile
        except UserProfile.DoesNotExist:
            raise ValueError("User profile not found")
        
        if not profile.gmail_connected or not profile.gmail_access_token:
            raise ValueError("Gmail not connected")
        
        # Check if token is still valid
        if profile.is_gmail_token_valid():
            return profile.gmail_access_token
        
        # Token expired, try to refresh
        if not profile.gmail_refresh_token:
            raise ValueError("No refresh token available")
        
        try:
            token_data = self.refresh_access_token(profile.gmail_refresh_token)
            
            # Update profile with new token
            expires_in = token_data.get('expires_in', 3600)
            expires_at = timezone.now() + timedelta(seconds=expires_in)
            
            profile.gmail_access_token = token_data.get('access_token')
            profile.gmail_token_expires_at = expires_at
            
            # Update refresh token if provided
            if 'refresh_token' in token_data:
                profile.gmail_refresh_token = token_data['refresh_token']
            
            profile.save()
            
            return profile.gmail_access_token
            
        except Exception as e:
            # Refresh failed, mark as disconnected
            profile.gmail_connected = False
            profile.save()
            raise ValueError(f"Failed to refresh token: {str(e)}")
    
    def send_email(self, user, subject, body, recipients, html_body=None):
        """Send email using Gmail OAuth2"""
        access_token = self.get_valid_access_token(user)
        
        # Get user's Gmail address
        try:
            profile = user.profile
            from_email = profile.gmail_email or user.email
        except UserProfile.DoesNotExist:
            from_email = user.email
        
        if not from_email:
            raise ValueError("No email address available for sending")
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = ', '.join(recipients) if isinstance(recipients, list) else recipients
        
        # Add text part
        text_part = MIMEText(body, 'plain', 'utf-8')
        msg.attach(text_part)
        
        # Add HTML part if provided
        if html_body:
            html_part = MIMEText(html_body, 'html', 'utf-8')
            msg.attach(html_part)
        
        # Encode message
        raw_message = base64.urlsafe_b64encode(msg.as_bytes()).decode('utf-8')
        
        # Send via Gmail API
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'raw': raw_message
        }
        
        response = requests.post(
            'https://gmail.googleapis.com/gmail/v1/users/me/messages/send',
            headers=headers,
            data=json.dumps(data)
        )
        
        response.raise_for_status()
        return response.json()
    
    def disconnect_gmail(self, user):
        """Disconnect Gmail and revoke tokens"""
        try:
            profile = user.profile
        except UserProfile.DoesNotExist:
            return
        
        if profile.gmail_access_token:
            try:
                # Revoke token
                requests.post(self.REVOKE_URL, data={'token': profile.gmail_access_token})
            except:
                pass  # Ignore revocation errors
        
        # Clear tokens from profile
        profile.gmail_access_token = None
        profile.gmail_refresh_token = None
        profile.gmail_token_expires_at = None
        profile.gmail_email = None
        profile.gmail_connected = False
        profile.save()
