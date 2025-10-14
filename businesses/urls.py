from django.urls import path
from .views import BusinessSearchView


urlpatterns = [
    path('', BusinessSearchView.as_view(), name='business_search'),
]


