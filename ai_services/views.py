from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .email_generator import EmailGenerator


class GenerateEmailView(APIView):
    """Generate AI-powered email content."""
    permission_classes = [permissions.IsAuthenticated]
    
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
    permission_classes = [permissions.IsAuthenticated]
    
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
