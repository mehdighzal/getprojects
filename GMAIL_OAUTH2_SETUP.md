# Gmail OAuth2 Setup Guide

This guide will help you set up Gmail OAuth2 integration for sending emails with your real Gmail account.

## Prerequisites

1. A Google Cloud Console account
2. A Gmail account
3. Django backend running

## Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Gmail API:
   - Go to "APIs & Services" > "Library"
   - Search for "Gmail API"
   - Click on it and enable it

## Step 2: Create OAuth2 Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth 2.0 Client IDs"
3. Choose "Web application" as the application type
4. Add authorized redirect URIs:
   - `http://localhost:8000/api/emails/gmail/callback/` (for development)
   - `https://yourdomain.com/api/emails/gmail/callback/` (for production)
5. Click "Create"
6. Copy the Client ID and Client Secret

## Step 3: Configure Environment Variables

Add these variables to your `.env` file:

```env
# Gmail OAuth2 Settings
GMAIL_CLIENT_ID=your-gmail-client-id-here
GMAIL_CLIENT_SECRET=your-gmail-client-secret-here
GMAIL_REDIRECT_URI=http://localhost:8000/api/emails/gmail/callback/
```

## Step 4: Test the Integration

1. Start your Django backend:
   ```bash
   python manage.py runserver
   ```

2. Start your React frontend:
   ```bash
   cd devlink-frontend
   npm start
   ```

3. Go to your profile page and click "Connect Gmail"
4. Complete the OAuth2 flow
5. Test sending an email

## How It Works

1. **User clicks "Connect Gmail"**: Frontend requests authorization URL from backend
2. **User authorizes**: Google redirects to your callback URL with authorization code
3. **Backend exchanges code for tokens**: Backend exchanges authorization code for access and refresh tokens
4. **Tokens stored securely**: Tokens are stored in the user's profile in the database
5. **Emails sent via Gmail API**: When sending emails, the system uses the stored tokens to authenticate with Gmail API

## Security Features

- **OAuth2 Flow**: Secure authentication without storing passwords
- **Token Refresh**: Access tokens are automatically refreshed when they expire
- **User Control**: Users can disconnect their Gmail account at any time
- **Secure Storage**: Tokens are stored encrypted in the database

## Troubleshooting

### Common Issues

1. **"Invalid redirect URI"**: Make sure the redirect URI in Google Cloud Console matches exactly
2. **"Client ID not found"**: Verify your Gmail Client ID is correct in the .env file
3. **"Token expired"**: The system should automatically refresh tokens, but you may need to reconnect

### Testing

You can test the Gmail integration by:
1. Connecting your Gmail account
2. Sending a test email from the profile page
3. Checking your Gmail sent folder

## Production Deployment

For production deployment:

1. Update the redirect URI to your production domain
2. Ensure your domain is verified in Google Cloud Console
3. Consider using environment-specific OAuth2 credentials
4. Set up proper logging and monitoring for OAuth2 flows

## API Endpoints

The following API endpoints are available for Gmail integration:

- `GET /api/emails/gmail/auth-url/` - Get authorization URL
- `GET /api/emails/gmail/callback/` - OAuth2 callback handler
- `GET /api/emails/gmail/status/` - Check connection status
- `POST /api/emails/gmail/disconnect/` - Disconnect Gmail
- `POST /api/emails/gmail/send/` - Send email via Gmail

## Support

If you encounter any issues, check:
1. Google Cloud Console for API quotas and errors
2. Django logs for backend errors
3. Browser console for frontend errors
4. Network tab for API call failures
