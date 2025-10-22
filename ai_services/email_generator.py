"""
AI Email Content Generation Service

This module provides AI-powered email content generation for developers
to reach out to local businesses.

Now includes automatic language detection based on business location:
Italy → Italian
France → French
Spain → Spanish
Morocco → Arabic
Germany → German
UK/US → English
"""

import os
import json
import re

try:
    import google.generativeai as genai  # type: ignore
except Exception:  # pragma: no cover
    genai = None


class EmailGenerator:
    """AI service for generating personalized email content with automatic language detection."""

    @staticmethod
    def get_user_info(user):
        """Extract user information from User and UserProfile models."""
        if not user or not user.is_authenticated:
            return {
                'full_name': 'Developer',
                'first_name': '',
                'last_name': '',
                'phone': '',
                'website_url': '',
                'github_url': '',
                'linkedin_url': '',
                'company': '',
                'job_title': '',
                'location': ''
            }

        try:
            profile = user.profile
        except:
            profile = None

        # Use the profile's full_name property if available, otherwise construct from User model
        if profile and hasattr(profile, 'full_name'):
            full_name = profile.full_name
        elif user.first_name and user.last_name:
            full_name = f"{user.first_name} {user.last_name}"
        elif user.first_name:
            full_name = user.first_name
        else:
            full_name = user.username

        return {
            'full_name': full_name,
            'first_name': user.first_name or '',
            'last_name': user.last_name or '',
            'phone': getattr(profile, 'phone', '') if profile else '',
            'website_url': getattr(profile, 'website_url', '') if profile else '',
            'github_url': getattr(profile, 'github_url', '') if profile else '',
            'linkedin_url': getattr(profile, 'linkedin_url', '') if profile else '',
            'company': getattr(profile, 'company', '') if profile else '',
            'job_title': getattr(profile, 'job_title', '') if profile else '',
            'location': getattr(profile, 'location', '') if profile else ''
        }

    @staticmethod
    def detect_language_from_location(location: str) -> str:
        """Detect email language automatically based on location (country or city string)."""
        if not location:
            return 'English'

        loc = location.lower().strip()
        if any(country in loc for country in ['italy', 'italia', 'pisa', 'milano', 'roma', 'napoli']):
            return 'Italian'
        elif any(country in loc for country in ['france', 'paris', 'lyon', 'marseille']):
            return 'French'
        elif any(country in loc for country in ['spain', 'españa', 'madrid', 'barcelona']):
            return 'Spanish'
        elif any(country in loc for country in ['morocco', 'maroc', 'casablanca', 'rabat', 'marrakech']):
            return 'Arabic'
        elif any(country in loc for country in ['germany', 'deutschland', 'berlin', 'munich', 'frankfurt']):
            return 'German'
        elif any(country in loc for country in ['united kingdom', 'england', 'london', 'uk', 'usa', 'united states', 'america']):
            return 'English'
        return 'English'

    @staticmethod
    def generate_intro_email(business_name, business_category, developer_name, developer_services,
                             user=None, business_country=None, business_city=None):
        """
        Generate an introductory email in the correct language based on the business location.
        """
        user_info = EmailGenerator.get_user_info(user)
        actual_name = user_info['full_name'] if user_info['full_name'] != 'Developer' else developer_name

        # Combine location fields
        location_str = f"{business_city or ''}, {business_country or ''}".strip(", ")
        target_language = EmailGenerator.detect_language_from_location(location_str)

        api_key = os.getenv('GEMINI_API_KEY', '')
        model_name = os.getenv('GEMINI_MODEL', 'models/gemini-2.0-flash')

        # Use Gemini AI if available
        if genai and api_key:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel(model_name)

                contact_info = []
                if user_info.get('phone'):
                    contact_info.append(f"Phone: {user_info['phone']}")
                if user_info.get('website_url'):
                    contact_info.append(f"Website: {user_info['website_url']}")
                if user_info.get('company'):
                    contact_info.append(f"Company: {user_info['company']}")
                if user_info.get('job_title'):
                    contact_info.append(f"Title: {user_info['job_title']}")
                contact_string = "\n".join(contact_info)

                location_context = f"Business located in {location_str}. Write in {target_language}."

                # Build business research context
                business_research_context = f"""
BUSINESS RESEARCH REQUIRED:
Before writing the email, you MUST research this business and analyze their needs:

1. RESEARCH THE BUSINESS: Search for information about {business_name} online to understand their business better
2. FIND REAL CONTACT NAMES: Try to find the actual name of the business owner/manager online
3. RESEARCH THE BUSINESS TYPE: What are common digital needs for {business_category} businesses?
4. IDENTIFY SPECIFIC PAIN POINTS: What challenges do {business_category} businesses typically face?
5. SUGGEST RELEVANT SOLUTIONS: What digital solutions would be most valuable for this type of business?
6. PERSONALIZE THE APPROACH: How can you tailor your services to their specific industry needs?

Business Name: {business_name}
Business Category: {business_category}
Location: {business_city or 'Unknown'}, {business_country or 'Unknown'}

IMPORTANT: If you find a real contact name, use it. If not, use simple "Gentile Sig.ra/Sig." - NEVER use placeholder text like "Ricerca il nome di un responsabile se disponibile online".
"""
                
                # Build contact information context (only include what exists)
                contact_context = "DEVELOPER CONTACT INFORMATION (ONLY include what is available):\n"
                if user_info.get('phone'):
                    contact_context += f"- Phone: {user_info['phone']}\n"
                if user_info.get('website_url'):
                    contact_context += f"- Website: {user_info['website_url']}\n"
                if user_info.get('github_url'):
                    contact_context += f"- GitHub: {user_info['github_url']}\n"
                if user_info.get('linkedin_url'):
                    contact_context += f"- LinkedIn: {user_info['linkedin_url']}\n"
                if user_info.get('company'):
                    contact_context += f"- Company: {user_info['company']}\n"
                if user_info.get('job_title'):
                    contact_context += f"- Title: {user_info['job_title']}\n"
                
                if contact_context == "DEVELOPER CONTACT INFORMATION (ONLY include what is available):\n":
                    contact_context += "- Only name is available\n"

                prompt = (
                    f"Write a professional outreach email FROM {actual_name} TO {business_name}.\n"
                    f"Category: {business_category}\n"
                    f"Developer offers: {developer_services}\n"
                    f"{location_context}\n\n"
                    f"{business_research_context}\n"
                    f"{contact_context}\n"
                    f"\nCRITICAL REQUIREMENTS:\n"
                    f"- Write the subject and body entirely in {target_language}\n"
                    f"- Use correct business etiquette for {target_language}\n"
                    f"- Use the name '{actual_name}' exactly as given\n"
                    f"- RESEARCH the business online to find real contact names if possible\n"
                    f"- If you find a real contact name, use it in the greeting\n"
                    f"- If no real name found, use simple 'Gentile Sig.ra/Sig.' or equivalent in {target_language}\n"
                    f"- NEVER use placeholder text like 'Ricerca il nome di un responsabile se disponibile online'\n"
                    f"- RESEARCH the business type and suggest relevant digital solutions\n"
                    f"- PERSONALIZE the email based on what {business_category} businesses typically need\n"
                    f"- Be specific about how you can help their business grow\n"
                    f"- Mention relevant services for their industry\n"
                    f"- Include ONLY the contact information that is actually available from the database\n"
                    f"- Do NOT include placeholder text like [Your Phone Number], [Your Website], or [Link to your website/portfolio]\n"
                    f"- Use ONLY real contact information from the developer's profile\n"
                    f"- End with a professional signature using only available contact information\n"
                    f"- Return valid JSON with keys 'subject' and 'body'\n"
                )

                resp = model.generate_content(prompt)
                text = resp.text or ''
                match = re.search(r"\{[\s\S]*\}", text)
                if match:
                    data = json.loads(match.group(0))
                    return {
                        'subject': data.get('subject', f"Partnership Opportunity - {business_name}"),
                        'body': data.get('body', ''),
                        'source': 'gemini'
                    }
            except Exception:
                pass  # fallback to template below

        # Build signature with real contact info
        signature_parts = [actual_name]
        if user_info.get('phone'):
            signature_parts.append(user_info['phone'])
        if user_info.get('website_url'):
            signature_parts.append(user_info['website_url'])
        if user_info.get('github_url'):
            signature_parts.append(user_info['github_url'])
        if user_info.get('company'):
            signature_parts.append(user_info['company'])
        signature = "\n".join(signature_parts)

        # Localized fallback templates
        if target_language == 'Italian':
            subject = f"Opportunità di Collaborazione - {business_name}"
            body = (
                f"Gentile Sig.ra/Sig.,\n\n"
                f"Mi chiamo {actual_name}, e mi occupo di {developer_services}.\n"
                f"Sarei felice di discutere come possiamo collaborare per migliorare la vostra presenza digitale.\n\n"
                f"Possiamo sentirci questa settimana?\n\n"
                f"Cordiali saluti,\n{signature}"
            )
        elif target_language == 'French':
            subject = f"Opportunité de Partenariat - {business_name}"
            body = (
                f"Madame, Monsieur,\n\n"
                f"Je m'appelle {actual_name}, et je suis spécialisé dans {developer_services}.\n"
                f"J'aimerais discuter d'une collaboration pour renforcer votre présence digitale.\n\n"
                f"Êtes-vous disponibles pour un appel cette semaine ?\n\n"
                f"Cordialement,\n{signature}"
            )
        elif target_language == 'Spanish':
            subject = f"Oportunidad de Colaboración - {business_name}"
            body = (
                f"Estimado/a Sr./Sra.,\n\n"
                f"Me llamo {actual_name}, y me especializo en {developer_services}.\n"
                f"Me encantaría hablar sobre cómo podríamos colaborar para mejorar su presencia digital.\n\n"
                f"¿Podemos agendar una breve llamada esta semana?\n\n"
                f"Atentamente,\n{signature}"
            )
        elif target_language == 'Arabic':
            subject = f"فرصة تعاون - {business_name}"
            body = (
                f"مرحبًا بفريق {business_name}،\n\n"
                f"اسمي {actual_name}، وأنا متخصص في {developer_services}.\n"
                f"يسعدني أن أتناقش معكم حول إمكانية التعاون لتعزيز حضوركم الرقمي.\n\n"
                f"هل يمكننا التحدث هذا الأسبوع؟\n\n"
                f"مع أطيب التحيات،\n{signature}"
            )
        elif target_language == 'German':
            subject = f"Partnerschaftsmöglichkeit - {business_name}"
            body = (
                f"Sehr geehrte Damen und Herren,\n\n"
                f"Mein Name ist {actual_name}, und ich bin spezialisiert auf {developer_services}.\n"
                f"Ich würde mich freuen, mit Ihnen über eine mögliche Zusammenarbeit zu sprechen.\n\n"
                f"Mit freundlichen Grüßen,\n{signature}"
            )
        else:
            subject = f"Partnership Opportunity - {business_name}"
            body = (
                f"Dear Sir/Madam,\n\n"
                f"My name is {actual_name}, and I specialize in {developer_services}.\n"
                f"I'd love to explore how we can collaborate to improve your digital presence.\n\n"
                f"Would you be open to a short call this week?\n\n"
                f"Best regards,\n{signature}"
            )


        return {'subject': subject, 'body': body, 'source': 'template'}

    @staticmethod
    def generate_bulk_email_template(category, developer_name, developer_services, user=None):
        """
        Generate a template for bulk emails to businesses in a specific category.
        """
        user_info = EmailGenerator.get_user_info(user)
        actual_name = user_info['full_name'] if user_info['full_name'] != 'Developer' else developer_name

        subject = f"Digital Solutions for {category.title()} Businesses"

        signature_parts = [actual_name]
        for field in ('company', 'phone', 'website'):
            val = user_info.get(field)
            if val:
                signature_parts.append(val)
        signature = "\n".join(signature_parts)

        body = (
            f"Dear Business Owner,\n\n"
            f"My name is {actual_name}, and I specialize in helping {category} businesses improve their digital presence.\n\n"
            f"I offer services such as:\n{developer_services}\n\n"
            f"I’d be happy to schedule a short call to see how I can help your business grow.\n\n"
            f"Best regards,\n{signature}\n\n"
            f"---\nThis email was generated using AI assistance."
        )

        return {'subject': subject, 'body': body}
