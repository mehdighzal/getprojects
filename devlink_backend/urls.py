"""
URL configuration for devlink_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.conf.urls.static import static
import urllib.parse
import os
import requests

def api_root(request):
    """Root endpoint showing available API routes."""
    return JsonResponse({
        'message': 'DevLink Backend API',
        'version': '1.0.0',
        'endpoints': {
            'auth': '/api/auth/',
            'businesses': '/api/businesses/',
            'emails': '/api/emails/',
            'ai': '/api/ai/',
            'admin': '/admin/'
        },
        'documentation': 'See README.md for detailed API documentation'
    })

 

def _gmail_auth_url():
    params = {
        'client_id': os.getenv('GOOGLE_CLIENT_ID', ''),
        'redirect_uri': os.getenv('GOOGLE_REDIRECT_URI', ''),
        'response_type': 'code',
        'scope': 'https://mail.google.com/ https://www.googleapis.com/auth/gmail.send https://www.googleapis.com/auth/userinfo.email',
        'access_type': 'offline',
        'prompt': 'consent',
    }
    return 'https://accounts.google.com/o/oauth2/v2/auth?' + urllib.parse.urlencode(params)

@csrf_exempt
def _gmail_oauth_callback(request):
    code = request.GET.get('code')
    if not code:
        return JsonResponse({'error': 'missing code'}, status=400)
    data = {
        'client_id': os.getenv('GOOGLE_CLIENT_ID', ''),
        'client_secret': os.getenv('GOOGLE_CLIENT_SECRET', ''),
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': os.getenv('GOOGLE_REDIRECT_URI', ''),
    }
    resp = requests.post('https://oauth2.googleapis.com/token', data=data, timeout=20)
    if resp.status_code != 200:
        return JsonResponse({'error': 'token_exchange_failed', 'details': resp.text}, status=400)
    payload = resp.json()
    return JsonResponse({
        'access_token': payload.get('access_token'),
        'refresh_token': payload.get('refresh_token'),
        'expires_in': payload.get('expires_in'),
        'set_env': {
            'EMAIL_AUTH_METHOD': 'gmail_oauth2',
            'EMAIL_HOST_USER': os.getenv('EMAIL_HOST_USER', ''),
            'GMAIL_OAUTH2_ACCESS_TOKEN': payload.get('access_token'),
        }
    })

urlpatterns = [
    path('', api_root, name='api_root'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/businesses/', include('businesses.urls')),
    path('api/emails/', include('emails.urls')),
    path('api/ai/', include('ai_services.urls')),
    path('oauth/gmail/start/', lambda r: HttpResponseRedirect(_gmail_auth_url()), name='gmail_oauth_start'),
    path('oauth/gmail/callback/', _gmail_oauth_callback, name='gmail_oauth_callback'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
