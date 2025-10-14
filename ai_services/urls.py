from django.urls import path
from .views import GenerateEmailView, GenerateBulkEmailView, GenerateBusinessesView, TestGeminiView


urlpatterns = [
    path('generate-email/', GenerateEmailView.as_view(), name='generate_email'),
    path('generate-bulk-email/', GenerateBulkEmailView.as_view(), name='generate_bulk_email'),
    path('generate-businesses/', GenerateBusinessesView.as_view(), name='generate_businesses'),
    path('test-gemini/', TestGeminiView.as_view(), name='test_gemini'),
]
