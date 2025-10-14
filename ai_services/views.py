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
    """Generate a list of plausible local businesses using AI (or fallback)."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        params = request.data or {}
        country = params.get('country', '')
        city = params.get('city', '')
        category = params.get('category', '')
        search = params.get('search', '')

        api_key = os.getenv('GEMINI_API_KEY', '')
        model_name = os.getenv('GEMINI_MODEL', 'models/gemini-2.0-flash')

        if genai and api_key:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel(model_name)
                prompt = (
                    "IMPORTANT: Generate 10 REALISTIC and PLAUSIBLE local business examples that could exist in the real world.\n"
                    f"Location: {city}, {country}\n"
                    f"Category: {category}\n"
                    f"Search term: {search}\n\n"
                    "Use realistic business names, addresses that follow the local format, and plausible contact details.\n"
                    "For emails: use realistic domain patterns (businessname@gmail.com, info@businessname.it, etc.)\n"
                    "For phone: use proper country/city format\n"
                    "For addresses: use real street name patterns for that city\n\n"
                    "Return ONLY a JSON array with these fields per business:\n"
                    "id (int), name (string), email (string), phone (string, optional), website (string, optional), category (string), country (string), city (string), address (string)\n\n"
                    "Example format: [{\"id\":1,\"name\":\"...\",\"email\":\"...\",\"phone\":\"...\",\"website\":\"...\",\"category\":\"...\",\"country\":\"...\",\"city\":\"...\",\"address\":\"...\"}]\n"
                    "Respond with ONLY the JSON array, no markdown, no extra text."
                )
                resp = model.generate_content(prompt)
                text = (resp.text or '').strip()
                import json, re
                match = re.search(r"\[[\s\S]*\]", text)
                data = json.loads(match.group(0) if match else text)
                # Basic validation and normalization
                normalized = []
                next_id = 1
                for item in data:
                    normalized.append({
                        'id': int(item.get('id', next_id)),
                        'name': item.get('name') or f"{category.title()} #{next_id}",
                        'email': item.get('email') or f"contact{next_id}@example.com",
                        'phone': item.get('phone') or '',
                        'website': item.get('website') or '',
                        'category': item.get('category') or category,
                        'country': item.get('country') or country,
                        'city': item.get('city') or city,
                        'address': item.get('address') or f"{city}"
                    })
                    next_id += 1
                return Response(normalized, status=200)
            except Exception:
                pass

        # Fallback deterministic sample
        sample = []
        for i in range(1, 11):
            sample.append({
                'id': i,
                'name': f"{category.title() or 'Business'} {city.title() or 'Local'} {i}",
                'email': f"info{i}@{(city or 'local').lower()}-{(category or 'business').lower()}.example.com",
                'phone': '',
                'website': '',
                'category': category or 'other',
                'country': country or 'unknown',
                'city': city or 'unknown',
                'address': f"{city or 'unknown'}"
            })
        return Response(sample, status=200)


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
