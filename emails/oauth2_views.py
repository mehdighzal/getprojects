"""
OAuth2 views for Gmail integration
"""
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .gmail_oauth2 import GmailOAuth2Service
from .models import EmailLog
import logging

logger = logging.getLogger(__name__)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def gmail_auth_url(request):
    """Get Gmail OAuth2 authorization URL"""
    try:
        oauth_service = GmailOAuth2Service()
        state = f"user_{request.user.id}"
        auth_url = oauth_service.get_authorization_url(state=state)
        
        return Response({
            'auth_url': auth_url,
            'message': 'Redirect user to this URL to authorize Gmail access'
        })
    except ValueError as e:
        # Configuration error
        logger.error(f"Gmail OAuth2 configuration error: {str(e)}")
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        logger.error(f"Error generating Gmail auth URL: {str(e)}")
        return Response(
            {'error': 'Failed to generate authorization URL'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([])  # No authentication required for OAuth2 callback
def gmail_callback(request):
    """Handle Gmail OAuth2 callback"""
    logger.info(f"Gmail callback received: code={request.GET.get('code', 'None')[:20]}..., state={request.GET.get('state')}, error={request.GET.get('error')}")
    
    try:
        code = request.GET.get('code')
        state = request.GET.get('state')
        error = request.GET.get('error')
        
        if error:
            return Response(
                {'error': f'OAuth2 error: {error}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not code:
            return Response(
                {'error': 'Authorization code not provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Extract user ID from state parameter
        if not state or not state.startswith('user_'):
            return Response(
                {'error': 'Invalid state parameter'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user_id = int(state.split('_')[1])
            user = User.objects.get(id=user_id)
            logger.info(f"Found user: {user.username} (ID: {user.id})")
        except (ValueError, User.DoesNotExist):
            logger.error(f"Invalid user in state parameter: {state}")
            return Response(
                {'error': 'Invalid user in state parameter'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        oauth_service = GmailOAuth2Service()
        
        # Exchange code for tokens
        logger.info("Exchanging code for tokens...")
        token_data = oauth_service.exchange_code_for_tokens(code)
        logger.info("Token exchange successful")
        
        # Get user info
        logger.info("Getting user info...")
        user_info = oauth_service.get_user_info(token_data['access_token'])
        logger.info(f"User info retrieved: {user_info.get('email')}")
        
        # Save tokens to user profile
        logger.info("Saving tokens to user profile...")
        profile = oauth_service.save_tokens_to_profile(
            user, 
            token_data, 
            user_info
        )
        logger.info(f"Tokens saved successfully. Profile connected: {profile.gmail_connected}")
        
        # Return HTML response that can close the popup window
        html_response = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Gmail Connected</title>
            <style>
                body {{ font-family: Arial, sans-serif; text-align: center; padding: 50px; }}
                .success {{ color: green; }}
                .message {{ margin: 20px 0; }}
            </style>
        </head>
        <body>
            <h1 class="success">Gmail Connected Successfully!</h1>
            <p class="message">You can now close this window and return to the application.</p>
            <p>Connected email: {user_info.get('email', 'Unknown')}</p>
            <script>
                // Send message to parent window
                if (window.opener) {{
                    window.opener.postMessage({{ type: 'GMAIL_CONNECTED' }}, window.location.origin);
                }}
                // Try to close the window
                window.close();
                // If window.close() doesn't work, show a message
                setTimeout(function() {{
                    document.body.innerHTML += '<p>Please close this window manually.</p>';
                }}, 2000);
            </script>
        </body>
        </html>
        """
        
        from django.http import HttpResponse
        return HttpResponse(html_response)
        
    except Exception as e:
        logger.error(f"Error in Gmail callback: {str(e)}")
        
        # Return HTML error response
        html_response = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Gmail Connection Error</title>
            <style>
                body {{ font-family: Arial, sans-serif; text-align: center; padding: 50px; }}
                .error {{ color: red; }}
                .message {{ margin: 20px 0; }}
            </style>
        </head>
        <body>
            <h1 class="error">Gmail Connection Failed</h1>
            <p class="message">There was an error connecting your Gmail account.</p>
            <p>Error: {str(e)}</p>
            <script>
                // Try to close the window
                window.close();
                // If window.close() doesn't work, show a message
                setTimeout(function() {{
                    document.body.innerHTML += '<p>Please close this window manually.</p>';
                }}, 2000);
            </script>
        </body>
        </html>
        """
        
        from django.http import HttpResponse
        return HttpResponse(html_response, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def gmail_status(request):
    """Check Gmail connection status"""
    try:
        profile = request.user.profile
        return Response({
            'connected': profile.gmail_connected,
            'email': profile.gmail_email,
            'token_valid': profile.is_gmail_token_valid() if profile.gmail_connected else False
        })
    except Exception as e:
        logger.error(f"Error checking Gmail status: {str(e)}")
        return Response({
            'connected': False,
            'email': None,
            'token_valid': False
        })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def gmail_disconnect(request):
    """Disconnect Gmail account"""
    try:
        oauth_service = GmailOAuth2Service()
        oauth_service.disconnect_gmail(request.user)
        
        return Response({
            'success': True,
            'message': 'Gmail disconnected successfully'
        })
    except Exception as e:
        logger.error(f"Error disconnecting Gmail: {str(e)}")
        return Response(
            {'error': f'Failed to disconnect Gmail: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_gmail_email(request):
    """Send email using Gmail OAuth2"""
    try:
        subject = request.data.get('subject')
        body = request.data.get('body')
        recipients = request.data.get('recipients', [])
        html_body = request.data.get('html_body')
        
        if not subject or not body or not recipients:
            return Response(
                {'error': 'Subject, body, and recipients are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if isinstance(recipients, str):
            recipients = [recipients]
        
        oauth_service = GmailOAuth2Service()
        
        # Send email via Gmail OAuth2
        result = oauth_service.send_email(
            user=request.user,
            subject=subject,
            body=body,
            recipients=recipients,
            html_body=html_body
        )
        
        # Log the email
        EmailLog.objects.create(
            user=request.user,
            subject=subject,
            body=body,
            recipients=','.join(recipients),
            status='sent'
        )
        
        return Response({
            'success': True,
            'message': f'Email sent successfully to {len(recipients)} recipients',
            'gmail_message_id': result.get('id')
        })
        
    except Exception as e:
        logger.error(f"Error sending Gmail email: {str(e)}")
        
        # Log failed email
        EmailLog.objects.create(
            user=request.user,
            subject=request.data.get('subject', ''),
            body=request.data.get('body', ''),
            recipients=','.join(request.data.get('recipients', [])),
            status='failed',
            error_message=str(e)
        )
        
        return Response(
            {'error': f'Failed to send email: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
