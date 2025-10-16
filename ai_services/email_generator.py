"""
AI Email Content Generation Service

This module provides AI-powered email content generation for developers
to reach out to local businesses.
"""


import os

try:
    import google.generativeai as genai  # type: ignore
except Exception:  # pragma: no cover
    genai = None


class EmailGenerator:
    """AI service for generating personalized email content.

    Uses Gemini via `google-generativeai` when `GEMINI_API_KEY` is set; otherwise
    falls back to a deterministic template.
    """
    
    @staticmethod
    def get_user_info(user):
        """Extract user information from User and UserProfile models."""
        if not user or not user.is_authenticated:
            return {
                'full_name': 'Developer',
                'first_name': '',
                'last_name': '',
                'phone': '',
                'website': '',
                'company': '',
                'job_title': '',
                'location': ''
            }
        
        # Get user profile if it exists
        try:
            profile = user.profile
        except:
            profile = None
        
        # Build full name from first_name and last_name, fallback to username
        if user.first_name and user.last_name:
            full_name = f"{user.first_name} {user.last_name}"
        elif user.first_name:
            full_name = user.first_name
        else:
            full_name = user.username
        
        return {
            'full_name': full_name,
            'first_name': user.first_name or '',
            'last_name': user.last_name or '',
            'phone': profile.phone if profile else '',
            'website': profile.website_url if profile else '',
            'company': profile.company if profile else '',
            'job_title': profile.job_title if profile else '',
            'location': profile.location if profile else ''
        }
    
    @staticmethod
    def generate_intro_email(business_name, business_category, developer_name, developer_services, user=None):
        """
        Generate an introductory email to a business.
        
        Args:
            business_name (str): Name of the business
            business_category (str): Category of the business
            developer_name (str): Name of the developer
            developer_services (str): Services offered by the developer
            user (User): Django User object to get profile information
            
        Returns:
            dict: Generated email content with subject and body
        """
        # Get user information
        user_info = EmailGenerator.get_user_info(user)
        
        # Use real name from database if available, otherwise use provided developer_name
        actual_name = user_info['full_name'] if user_info['full_name'] != 'Developer' else developer_name
        
        api_key = os.getenv('GEMINI_API_KEY', '')
        model_name = os.getenv('GEMINI_MODEL', 'models/gemini-2.0-flash')

        if genai and api_key:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel(model_name)
                
                # Build contact information string
                contact_info = []
                if user_info['phone']:
                    contact_info.append(f"Phone: {user_info['phone']}")
                if user_info['website']:
                    contact_info.append(f"Website: {user_info['website']}")
                if user_info['company']:
                    contact_info.append(f"Company: {user_info['company']}")
                if user_info['job_title']:
                    contact_info.append(f"Title: {user_info['job_title']}")
                
                contact_string = "\n".join(contact_info) if contact_info else ""
                
                prompt = (
                    f"Write a professional outreach email FROM {actual_name} (a developer) TO {business_name} (a {business_category} business).\n"
                    f"The developer offers: {developer_services}\n"
                    f"Developer's contact information:\n{contact_string}\n"
                    f"The email should:\n"
                    f"- Be written from the developer's perspective using their real name: {actual_name}\n"
                    f"- Introduce the developer and their services\n"
                    f"- Express interest in helping the business with their digital needs\n"
                    f"- Request a brief meeting or call\n"
                    f"- Be professional, concise, and friendly\n"
                    f"- Include contact information only if available (phone, website, etc.)\n"
                    f"- Do NOT include placeholder text like [Your Phone Number] or [Your Website]\n"
                    f"Return ONLY valid JSON with keys 'subject' and 'body'. Example: {{\"subject\":\"...\",\"body\":\"...\"}}"
                )
                resp = model.generate_content(prompt)
                text = resp.text or ''
                # Very simple parse: attempt to find JSON like {"subject":..., "body":...}
                import json, re
                match = re.search(r"\{[\s\S]*\}", text)
                if match:
                    data = json.loads(match.group(0))
                    subject = data.get('subject') or f"Partnership Opportunity - {business_name}"
                    body = data.get('body') or ''
                else:
                    subject = f"Partnership Opportunity - {business_name}"
                    body = text.strip()
                if not body:
                    body = f"Hello {business_name}, this is {developer_name}. I offer {developer_services}. I'd love to discuss how I can help your {business_category} business."
                return {'subject': subject, 'body': body, 'source': 'gemini'}
            except Exception:
                # Fall back to template if API fails
                pass

        subject = f"Partnership Opportunity - {business_name}"
        
        # Build signature with contact information
        signature_parts = [actual_name]
        if user_info['company']:
            signature_parts.append(user_info['company'])
        if user_info['phone']:
            signature_parts.append(user_info['phone'])
        if user_info['website']:
            signature_parts.append(user_info['website'])
        
        signature = "\n".join(signature_parts)
        
        body = (
            f"Dear {business_name} Team,\n\n"
            f"My name is {actual_name}, and I specialize in {developer_services}.\n\n"
            f"I was impressed by your {business_category} work and would love to explore how we could collaborate to enhance your digital presence.\n\n"
            f"Would you be open to a brief call this week?\n\n"
            f"Best regards,\n{signature}"
        )
        return {'subject': subject, 'body': body, 'source': 'template'}
    
    @staticmethod
    def generate_bulk_email_template(category, developer_name, developer_services, user=None):
        """
        Generate a template for bulk emails to businesses in a specific category.
        
        Args:
            category (str): Business category
            developer_name (str): Name of the developer
            developer_services (str): Services offered by the developer
            user (User): Django User object to get profile information
            
        Returns:
            dict: Template email content
        """
        # Get user information
        user_info = EmailGenerator.get_user_info(user)
        
        # Use real name from database if available, otherwise use provided developer_name
        actual_name = user_info['full_name'] if user_info['full_name'] != 'Developer' else developer_name
        subject = f"Digital Solutions for {category.title()} Businesses"
        
        # Build signature with contact information
        signature_parts = [actual_name]
        if user_info['company']:
            signature_parts.append(user_info['company'])
        if user_info['phone']:
            signature_parts.append(user_info['phone'])
        if user_info['website']:
            signature_parts.append(user_info['website'])
        
        signature = "\n".join(signature_parts)
        
        body = f"""Dear Business Owner,

I hope this message finds you well. My name is {actual_name}, and I'm a developer who specializes in helping {category} businesses like yours enhance their digital presence.

I understand the unique challenges that {category} businesses face in today's digital landscape, and I'm here to offer solutions that can help you:

{developer_services}

I've worked with several businesses in your industry and have seen significant improvements in their online presence, customer engagement, and operational efficiency.

Would you be interested in a brief consultation to discuss how I might be able to help your business grow?

I'm available for a 15-minute call this week to discuss your specific needs and how my services could benefit your business.

Thank you for your time, and I look forward to the possibility of working together.

Best regards,
{signature}

---
This email was generated using AI assistance to help developers connect with local businesses."""
        
        return {
            'subject': subject,
            'body': body
        }
