"""
Google Places API Service
Fetches real business data from Google Places API
"""
import os
import random
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
        Search for real businesses using Google Places API with randomization
        
        Args:
            city: City name
            country: Country name
            category: Business category/type
            search: Additional search keywords
            radius: Search radius in meters (default 5000m = 5km)
            
        Returns:
            List of business dictionaries (randomized each time)
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
            
            # Get multiple result sets using different strategies for variety
            all_results = []
            
            # Strategy 1: Text search with main query
            if search or not place_type:
                places_result = self.client.places(
                    query=f"{query} in {location_query}",
                    location=(lat, lng),
                    radius=radius
                )
                all_results.extend(places_result.get('results', []))
            else:
                # Strategy 1: Nearby search with type
                places_result = self.client.places_nearby(
                    location=(lat, lng),
                    radius=radius,
                    type=place_type,
                    keyword=query
                )
                all_results.extend(places_result.get('results', []))
            
            # Strategy 2: Additional searches with variations for more variety
            search_variations = [
                f"{category} near {location_query}" if category else None,
                f"{query} {city}" if city else None,
                f"best {category} {city}" if category and city else None,
                f"top {query} {location_query}" if query else None,
            ]
            
            for variation in search_variations:
                if variation and len(all_results) < 30:  # Limit to avoid too many API calls
                    try:
                        var_result = self.client.places(
                            query=variation,
                            location=(lat, lng),
                            radius=radius
                        )
                        all_results.extend(var_result.get('results', []))
                    except:
                        continue
            
            # Remove duplicates based on place_id
            seen_place_ids = set()
            unique_results = []
            for result in all_results:
                place_id = result.get('place_id')
                if place_id and place_id not in seen_place_ids:
                    seen_place_ids.add(place_id)
                    unique_results.append(result)
            
            # Randomize the results to get different businesses each time
            random.shuffle(unique_results)
            
            # Take up to 15 results (more variety)
            selected_results = unique_results[:15]
            
            # Format results
            businesses = []
            for idx, place in enumerate(selected_results):
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
    
    def search_businesses_with_pagination(
        self, 
        city: str = '', 
        country: str = '', 
        category: str = '', 
        search: str = '',
        radius: int = 5000,
        page: int = 0
    ) -> List[Dict]:
        """
        Search for businesses with pagination support for even more variety
        
        Args:
            city: City name
            country: Country name
            category: Business category/type
            search: Additional search keywords
            radius: Search radius in meters
            page: Page number (0-based) for pagination
            
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
            
            # Use different search strategies based on page number
            search_strategies = [
                f"{query} in {location_query}",
                f"{category} {city}" if category and city else f"{query} {city}",
                f"best {category} {location_query}" if category else f"top {query} {location_query}",
                f"{query} near {location_query}",
                f"popular {category} {city}" if category and city else f"recommended {query} {city}",
            ]
            
            # Select strategy based on page number
            strategy_index = page % len(search_strategies)
            selected_strategy = search_strategies[strategy_index]
            
            # Add some randomization to the query
            random_modifiers = ["", " popular", " best", " top rated", " recommended"]
            random_modifier = random.choice(random_modifiers)
            final_query = selected_strategy + random_modifier
            
            # Search places
            places_result = self.client.places(
                query=final_query,
                location=(lat, lng),
                radius=radius
            )
            
            results = places_result.get('results', [])
            
            # Randomize results
            random.shuffle(results)
            
            # Take up to 12 results
            selected_results = results[:12]
            
            # Format results
            businesses = []
            for idx, place in enumerate(selected_results):
                business = self._format_place(place, idx + 1, city, country, category)
                businesses.append(business)
            
            return businesses
            
        except Exception as e:
            print(f"Google Places API Error: {str(e)}")
            return []

