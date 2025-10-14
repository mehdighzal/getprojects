from rest_framework import generics, permissions, filters
from .models import Business
from .serializers import BusinessSerializer


class BusinessSearchView(generics.ListCreateAPIView):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'city', 'country', 'category']

    def get_queryset(self):
        queryset = super().get_queryset()
        country = self.request.query_params.get('country')
        city = self.request.query_params.get('city')
        category = self.request.query_params.get('category')
        if country:
            queryset = queryset.filter(country__iexact=country)
        if city:
            queryset = queryset.filter(city__iexact=city)
        if category:
            queryset = queryset.filter(category=category)
        return queryset


# Create your views here.
