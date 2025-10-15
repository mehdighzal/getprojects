from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from .serializers import UserSerializer, UserUpdateSerializer, ChangePasswordSerializer


class UserProfileView(APIView):
    """Get and update user profile."""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get current user profile."""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def put(self, request):
        """Update current user profile."""
        serializer = UserUpdateSerializer(request.user, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    """Change user password."""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Change user password."""
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'message': 'Password changed successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserStatsView(APIView):
    """Get user statistics."""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get user email statistics."""
        from emails.models import EmailLog
        
        user = request.user
        
        # Get email statistics
        total_emails = EmailLog.objects.filter(user=user).count()
        
        # This month
        from datetime import datetime, timedelta
        from django.utils import timezone
        
        now = timezone.now()
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        emails_this_month = EmailLog.objects.filter(
            user=user, 
            created_at__gte=start_of_month
        ).count()
        
        # This week
        start_of_week = now - timedelta(days=now.weekday())
        start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
        emails_this_week = EmailLog.objects.filter(
            user=user, 
            created_at__gte=start_of_week
        ).count()
        
        # Unique recipients
        unique_recipients = EmailLog.objects.filter(user=user).values_list('recipients', flat=True)
        unique_count = set()
        for recipients in unique_recipients:
            if recipients:
                unique_count.update(recipients.split(','))
        
        # Last email date
        last_email = EmailLog.objects.filter(user=user).order_by('-created_at').first()
        last_email_date = last_email.created_at if last_email else None
        
        stats = {
            'total_emails': total_emails,
            'emails_this_month': emails_this_month,
            'emails_this_week': emails_this_week,
            'unique_recipients': len(unique_count),
            'last_email_date': last_email_date,
        }
        
        return Response(stats)