from django.urls import path
from .views import (
    SendEmailView, EmailHistoryView, EmailTemplateListCreateView, 
    EmailTemplateDetailView, BulkEmailCampaignListCreateView,
    BulkEmailCampaignDetailView, BulkEmailCampaignSendView,
    CreateBulkCampaignFromBusinessesView, EmailAnalyticsView, EmailAnalyticsUpdateView
)


urlpatterns = [
    # Basic email operations
    path('send/', SendEmailView.as_view(), name='send_email'),
    path('history/', EmailHistoryView.as_view(), name='email_history'),
    
    # Email templates
    path('templates/', EmailTemplateListCreateView.as_view(), name='template_list_create'),
    path('templates/<int:pk>/', EmailTemplateDetailView.as_view(), name='template_detail'),
    
    # Bulk email campaigns
    path('campaigns/', BulkEmailCampaignListCreateView.as_view(), name='campaign_list_create'),
    path('campaigns/<int:pk>/', BulkEmailCampaignDetailView.as_view(), name='campaign_detail'),
    path('campaigns/<int:pk>/send/', BulkEmailCampaignSendView.as_view(), name='campaign_send'),
    path('campaigns/create-from-businesses/', CreateBulkCampaignFromBusinessesView.as_view(), name='create_campaign_from_businesses'),
    
    # Analytics
    path('analytics/', EmailAnalyticsView.as_view(), name='email_analytics'),
    path('analytics/update/', EmailAnalyticsUpdateView.as_view(), name='analytics_update'),
]


