from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .email_generator import EmailGenerator
import os
try:
    import google.generativeai as genai  # type: ignore
except Exception:
    genai = None


class GenerateEmailView(APIView):
    """Generate AI-powered email content."""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        """Generate email content based on business and developer info."""
        data = request.data
        
        # Extract parameters
        business_name = data.get('business_name', '')
        business_category = data.get('business_category', '')
        developer_name = data.get('developer_name', request.user.username)
        developer_services = data.get('developer_services', 'Web development and digital solutions')
        
        # Generate email content
        email_content = EmailGenerator.generate_intro_email(
            business_name=business_name,
            business_category=business_category,
            developer_name=developer_name,
            developer_services=developer_services
        )
        
        return Response(email_content, status=status.HTTP_200_OK)


class GenerateBulkEmailView(APIView):
    """Generate AI-powered bulk email template."""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        """Generate bulk email template for a business category."""
        data = request.data
        
        # Extract parameters
        category = data.get('category', '')
        developer_name = data.get('developer_name', request.user.username)
        developer_services = data.get('developer_services', 'Web development and digital solutions')
        
        # Generate email template
        email_content = EmailGenerator.generate_bulk_email_template(
            category=category,
            developer_name=developer_name,
            developer_services=developer_services
        )
        
        return Response(email_content, status=status.HTTP_200_OK)


class GenerateBusinessesView(APIView):
    """Fetch real businesses from Google Places API with randomization."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        from businesses.google_places_service import GooglePlacesService
        import random
        
        params = request.data or {}
        country = params.get('country', '')
        city = params.get('city', '')
        category = params.get('category', '')
        search = params.get('search', '')
        page = params.get('page', 0)  # Add page parameter for pagination

        # Use Google Places API for real business data
        places_service = GooglePlacesService()
        
        # Randomly choose between different search methods for variety
        search_methods = [
            lambda: places_service.search_businesses(
                city=city,
                country=country,
                category=category,
                search=search
            ),
            lambda: places_service.search_businesses_with_pagination(
                city=city,
                country=country,
                category=category,
                search=search,
                page=page
            )
        ]
        
        # Randomly select a search method
        selected_method = random.choice(search_methods)
        businesses = selected_method()
        
        if businesses:
            return Response(businesses, status=200)
        
        # If no Google API key, return empty array with error in console
        if not os.getenv('GOOGLE_PLACES_API_KEY'):
            print('ERROR: Google Places API key not configured')
            print('Please add GOOGLE_PLACES_API_KEY to your .env file')
            print('Setup guide: https://developers.google.com/maps/documentation/places/web-service/get-api-key')
            return Response([], status=200)
        
        # No results found - return empty array
        print(f'No businesses found for: {city}, {country} - {category}')
        return Response([], status=200)


class TestGeminiView(APIView):
    """Quick health-check for Gemini credentials and connectivity."""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        api_key = os.getenv('GEMINI_API_KEY', '')
        model_name = os.getenv('GEMINI_MODEL', 'models/gemini-2.0-flash')
        if not api_key:
            return Response({'ok': False, 'error': 'GEMINI_API_KEY missing'}, status=400)
        if not genai:
            return Response({'ok': False, 'error': 'google-generativeai not installed'}, status=500)
        try:
            genai.configure(api_key=api_key)
            # List available models
            available_models = []
            try:
                for m in genai.list_models():
                    if 'generateContent' in m.supported_generation_methods:
                        available_models.append(m.name)
            except:
                pass
            
            model = genai.GenerativeModel(model_name)
            resp = model.generate_content('ping')
            text = (getattr(resp, 'text', None) or '').strip()
            return Response({'ok': True, 'model': model_name, 'sample': text[:80], 'available_models': available_models[:10]}, status=200)
        except Exception as e:
            return Response({'ok': False, 'error': str(e), 'available_models': available_models[:10] if 'available_models' in locals() else []}, status=500)
