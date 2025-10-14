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
    def generate_intro_email(business_name, business_category, developer_name, developer_services):
        """
        Generate an introductory email to a business.
        
        Args:
            business_name (str): Name of the business
            business_category (str): Category of the business
            developer_name (str): Name of the developer
            developer_services (str): Services offered by the developer
            
        Returns:
            dict: Generated email content with subject and body
        """
        api_key = os.getenv('GEMINI_API_KEY', '')
        model_name = os.getenv('GEMINI_MODEL', 'models/gemini-2.0-flash')

        if genai and api_key:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel(model_name)
                prompt = (
                    f"Write a professional outreach email FROM {developer_name} (a developer) TO {business_name} (a {business_category} business).\n"
                    f"The developer offers: {developer_services}\n"
                    f"The email should:\n"
                    f"- Be written from the developer's perspective\n"
                    f"- Introduce the developer and their services\n"
                    f"- Express interest in helping the business with their digital needs\n"
                    f"- Request a brief meeting or call\n"
                    f"- Be professional, concise, and friendly\n"
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
        body = (
            f"Dear {business_name} Team,\n\n"
            f"My name is {developer_name}, and I specialize in {developer_services}.\n\n"
            f"I was impressed by your {business_category} work and would love to explore how we could collaborate to enhance your digital presence.\n\n"
            f"Would you be open to a brief call this week?\n\n"
            f"Best regards,\n{developer_name}"
        )
        return {'subject': subject, 'body': body, 'source': 'template'}
    
    @staticmethod
    def generate_bulk_email_template(category, developer_name, developer_services):
        """
        Generate a template for bulk emails to businesses in a specific category.
        
        Args:
            category (str): Business category
            developer_name (str): Name of the developer
            developer_services (str): Services offered by the developer
            
        Returns:
            dict: Template email content
        """
        subject = f"Digital Solutions for {category.title()} Businesses"
        
        body = f"""Dear Business Owner,

I hope this message finds you well. My name is {developer_name}, and I'm a developer who specializes in helping {category} businesses like yours enhance their digital presence.

I understand the unique challenges that {category} businesses face in today's digital landscape, and I'm here to offer solutions that can help you:

{developer_services}

I've worked with several businesses in your industry and have seen significant improvements in their online presence, customer engagement, and operational efficiency.

Would you be interested in a brief consultation to discuss how I might be able to help your business grow?

I'm available for a 15-minute call this week to discuss your specific needs and how my services could benefit your business.

Thank you for your time, and I look forward to the possibility of working together.

Best regards,
{developer_name}

---
This email was generated using AI assistance to help developers connect with local businesses."""
        
        return {
            'subject': subject,
            'body': body
        }
