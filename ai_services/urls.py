from django.urls import path
from .views import GenerateEmailView, GenerateBulkEmailView


urlpatterns = [
    path('generate-email/', GenerateEmailView.as_view(), name='generate_email'),
    path('generate-bulk-email/', GenerateBulkEmailView.as_view(), name='generate_bulk_email'),
]
