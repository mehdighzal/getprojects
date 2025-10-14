"""
Google Places API Service
Fetches real business data from Google Places API
"""
import os
from typing import List, Dict, Optional
import googlemaps
from django.conf import settings


class GooglePlacesService:
    """Service to interact with Google Places API"""
    
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_PLACES_API_KEY', '')
        self.client = None
        if self.api_key:
            self.client = googlemaps.Client(key=self.api_key)
    
    def search_businesses(
        self, 
        city: str = '', 
        country: str = '', 
        category: str = '', 
        search: str = '',
        radius: int = 5000
    ) -> List[Dict]:
        """
        Search for real businesses using Google Places API
        
        Args:
            city: City name
            country: Country name
            category: Business category/type
            search: Additional search keywords
            radius: Search radius in meters (default 5000m = 5km)
            
        Returns:
            List of business dictionaries
        """
        if not self.client:
            return []
        
        try:
            # Build location query
            location_query = f"{city}, {country}" if city and country else city or country
            
            # Get coordinates for the location
            if location_query:
                geocode_result = self.client.geocode(location_query)
                if not geocode_result:
                    return []
                
                location = geocode_result[0]['geometry']['location']
                lat, lng = location['lat'], location['lng']
            else:
                return []
            
            # Map category to Google Places type
            place_type = self._map_category_to_type(category)
            
            # Build search query
            query = search or category or 'business'
            
            # Search places using text search (more flexible)
            if search or not place_type:
                places_result = self.client.places(
                    query=f"{query} in {location_query}",
                    location=(lat, lng),
                    radius=radius
                )
            else:
                # Use nearby search with type
                places_result = self.client.places_nearby(
                    location=(lat, lng),
                    radius=radius,
                    type=place_type,
                    keyword=query
                )
            
            # Format results
            businesses = []
            for idx, place in enumerate(places_result.get('results', [])[:10]):
                business = self._format_place(place, idx + 1, city, country, category)
                businesses.append(business)
            
            return businesses
            
        except Exception as e:
            print(f"Google Places API Error: {str(e)}")
            return []
    
    def _map_category_to_type(self, category: str) -> Optional[str]:
        """Map our categories to Google Places types"""
        category_mapping = {
            'restaurant': 'restaurant',
            'club': 'night_club',
            'real_estate': 'real_estate_agency',
            'travel_agency': 'travel_agency',
            'medical': 'doctor',
            'technical_studio': 'general_contractor',
            'dentist': 'dentist',
            'physiotherapist': 'physiotherapist',
            'private_school': 'school',
            'beauty_center': 'beauty_salon',
            'artisan': 'store',
            'other': None
        }
        return category_mapping.get(category.lower())
    
    def _format_place(self, place: Dict, idx: int, city: str, country: str, category: str) -> Dict:
        """Format Google Place data to our business format"""
        place_id = place.get('place_id', '')
        name = place.get('name', f'Business {idx}')
        
        # Get detailed place info for contact details
        details = {}
        if place_id and self.client:
            try:
                details = self.client.place(place_id, fields=[
                    'name', 'formatted_address', 'formatted_phone_number', 
                    'website', 'types'
                ]).get('result', {})
            except:
                pass
        
        # Extract contact information
        address = details.get('formatted_address') or place.get('vicinity', '')
        phone = details.get('formatted_phone_number', '')
        website = details.get('website', '')
        
        # Generate email from business name (most businesses don't publicly list email)
        email = self._generate_email(name, website)
        
        # Get business types
        types = details.get('types', place.get('types', []))
        business_category = category or (types[0].replace('_', ' ') if types else 'other')
        
        return {
            'id': idx,
            'name': name,
            'email': email,
            'phone': phone,
            'website': website,
            'category': business_category,
            'country': country,
            'city': city,
            'address': address,
            'place_id': place_id,  # Extra: Google Place ID for reference
            'rating': place.get('rating', 0),  # Extra: rating
            'user_ratings_total': place.get('user_ratings_total', 0)  # Extra: review count
        }
    
    def _generate_email(self, business_name: str, website: str = '') -> str:
        """Generate a plausible email address"""
        if website:
            # Extract domain from website
            try:
                from urllib.parse import urlparse
                domain = urlparse(website).netloc
                if domain:
                    return f"info@{domain}"
            except:
                pass
        
        # Fallback: generate from business name
        clean_name = business_name.lower().replace(' ', '').replace("'", '')[:20]
        return f"info@{clean_name}.com"

