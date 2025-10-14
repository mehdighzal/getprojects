from django.urls import path
from .views import SendEmailView, EmailHistoryView


urlpatterns = [
    path('send/', SendEmailView.as_view(), name='send_email'),
    path('history/', EmailHistoryView.as_view(), name='email_history'),
]


