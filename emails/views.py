from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import datetime, timedelta
import os
import base64
import smtplib
import threading
from email.mime.text import MIMEText
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import (
    SendEmailSerializer, EmailLogSerializer, EmailTemplateSerializer,
    BulkEmailCampaignSerializer, EmailAnalyticsSerializer
)
from .models import EmailLog, EmailTemplate, BulkEmailCampaign, EmailAnalytics


class SendEmailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = SendEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        subject = serializer.validated_data['subject']
        body = serializer.validated_data['body']
        recipients = serializer.validated_data['recipients']

        auth_method = os.getenv('EMAIL_AUTH_METHOD', 'basic')  # basic | gmail_oauth2 | outlook_oauth2

        if auth_method == 'basic':
            # Send via configured backend (console by default or SMTP with app password)
            send_mail(subject, body, settings.EMAIL_HOST_USER or None, recipients, fail_silently=False)
        else:
            # OAuth2 over SMTP
            smtp_host = settings.EMAIL_HOST
            smtp_port = settings.EMAIL_PORT

            if auth_method == 'gmail_oauth2':
                access_token = os.getenv('GMAIL_OAUTH2_ACCESS_TOKEN', '')
                if not access_token:
                    return Response({'detail': 'GMAIL_OAUTH2_ACCESS_TOKEN missing'}, status=400)
                auth_string = f"user={settings.EMAIL_HOST_USER}\1auth=Bearer {access_token}\1\1"
            elif auth_method == 'outlook_oauth2':
                access_token = os.getenv('OUTLOOK_OAUTH2_ACCESS_TOKEN', '')
                if not access_token:
                    return Response({'detail': 'OUTLOOK_OAUTH2_ACCESS_TOKEN missing'}, status=400)
                auth_string = f"user={settings.EMAIL_HOST_USER}\1auth=Bearer {access_token}\1\1"
            else:
                return Response({'detail': 'Unsupported EMAIL_AUTH_METHOD'}, status=400)

            msg = MIMEText(body, _charset='utf-8')
            msg['Subject'] = subject
            msg['From'] = settings.EMAIL_HOST_USER
            msg['To'] = ', '.join(recipients)

            with smtplib.SMTP(smtp_host, smtp_port) as server:
                if settings.EMAIL_USE_TLS:
                    server.starttls()
                # XOAUTH2
                server.ehlo()
                server.docmd('AUTH', 'XOAUTH2 ' + base64.b64encode(auth_string.encode()).decode())
                server.sendmail(settings.EMAIL_HOST_USER, recipients, msg.as_string())

        EmailLog.objects.create(
            user=request.user,
            subject=subject,
            body=body,
            recipients=','.join(recipients),
        )

        return Response({'sent': len(recipients)}, status=status.HTTP_200_OK)



class EmailHistoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        qs = EmailLog.objects.filter(user=request.user).order_by('-created_at')
        # Simple cursor-less pagination via query params
        try:
            page = int(request.query_params.get('page', '1'))
            page_size = int(request.query_params.get('page_size', '10'))
        except ValueError:
            page, page_size = 1, 10

        start = (page - 1) * page_size
        end = start + page_size
        total = qs.count()

        items = qs[start:end]
        data = EmailLogSerializer(items, many=True).data
        return Response({
            'results': data,
            'page': page,
            'page_size': page_size,
            'total': total,
        })


# Email Templates Views
class EmailTemplateListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EmailTemplateSerializer

    def get_queryset(self):
        return EmailTemplate.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EmailTemplateDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EmailTemplateSerializer

    def get_queryset(self):
        return EmailTemplate.objects.filter(user=self.request.user)


# Bulk Email Campaign Views
class BulkEmailCampaignListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BulkEmailCampaignSerializer

    def get_queryset(self):
        return BulkEmailCampaign.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BulkEmailCampaignDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BulkEmailCampaignSerializer

    def get_queryset(self):
        return BulkEmailCampaign.objects.filter(user=self.request.user)


class BulkEmailCampaignSendView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            campaign = BulkEmailCampaign.objects.get(pk=pk, user=request.user)
        except BulkEmailCampaign.DoesNotExist:
            return Response({'detail': 'Campaign not found'}, status=404)

        if campaign.status != 'draft':
            return Response({'detail': 'Campaign is not in draft status'}, status=400)

        # Start sending in background thread
        campaign.status = 'sending'
        campaign.started_at = timezone.now()
        campaign.total_count = len(campaign.recipients)
        campaign.save()

        # Start background thread for sending
        thread = threading.Thread(target=self._send_bulk_emails, args=(campaign,))
        thread.daemon = True
        thread.start()

        return Response({'detail': 'Bulk email sending started with AI generation'}, status=200)

    def _send_bulk_emails(self, campaign):
        """Background task to send bulk emails with AI generation"""
        try:
            from ai_services.email_generator import EmailGenerator
            
            for i, recipient_data in enumerate(campaign.recipients):
                try:
                    # Generate AI email for this specific business
                    business_name = recipient_data.get('name', 'Business')
                    business_category = recipient_data.get('category', 'business')
                    
                    # Use AI to generate personalized email
                    ai_email = EmailGenerator.generate_intro_email(
                        business_name=business_name,
                        business_category=business_category,
                        developer_name=campaign.user.username or 'Developer',
                        developer_services='Web development and digital solutions'
                    )
                    
                    # Use AI-generated subject and body, or fallback to campaign defaults
                    email_subject = ai_email.get('subject', campaign.subject)
                    email_body = ai_email.get('body', campaign.body)
                    
                    # Send individual email
                    send_mail(
                        email_subject,
                        email_body,
                        settings.EMAIL_HOST_USER or None,
                        [recipient_data.get('email', '')],
                        fail_silently=False
                    )
                    
                    # Log the email with AI generation info
                    EmailLog.objects.create(
                        user=campaign.user,
                        subject=email_subject,
                        body=email_body,
                        recipients=recipient_data.get('email', ''),
                        status='sent'
                    )
                    
                    campaign.sent_count += 1
                    campaign.save()
                    
                except Exception as e:
                    # Log failed email
                    EmailLog.objects.create(
                        user=campaign.user,
                        subject=campaign.subject,
                        body=campaign.body,
                        recipients=recipient_data.get('email', ''),
                        status='failed',
                        error_message=str(e)
                    )

            # Mark campaign as completed
            campaign.status = 'completed'
            campaign.completed_at = timezone.now()
            campaign.save()

        except Exception as e:
            campaign.status = 'failed'
            campaign.error_message = str(e)
            campaign.save()


class CreateBulkCampaignFromBusinessesView(APIView):
    """Create a bulk campaign from business search results"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        businesses = request.data.get('businesses', [])
        campaign_name = request.data.get('name', f'Bulk Campaign {timezone.now().strftime("%Y-%m-%d %H:%M")}')
        
        if not businesses:
            return Response({'detail': 'No businesses provided'}, status=400)

        # Create campaign with businesses as recipients
        campaign = BulkEmailCampaign.objects.create(
            user=request.user,
            name=campaign_name,
            subject='AI-Generated Personalized Email',  # Will be overridden by AI
            body='This email will be personalized by AI for each business.',  # Will be overridden by AI
            recipients=businesses,
            status='draft'
        )

        return Response({
            'detail': 'Bulk campaign created successfully',
            'campaign_id': campaign.id,
            'recipients_count': len(businesses)
        }, status=201)


# Analytics Views
class EmailAnalyticsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Get date range from query params
        days = int(request.query_params.get('days', 30))
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=days)

        # Get analytics data
        analytics_data = EmailAnalytics.objects.filter(
            user=request.user,
            date__range=[start_date, end_date]
        ).order_by('date')

        # Get summary stats
        total_emails = EmailLog.objects.filter(
            user=request.user,
            created_at__date__range=[start_date, end_date]
        ).count()

        total_campaigns = BulkEmailCampaign.objects.filter(
            user=request.user,
            created_at__date__range=[start_date, end_date]
        ).count()

        # Get top templates
        top_templates = EmailTemplate.objects.filter(
            user=request.user
        ).annotate(
            usage_count=Count('bulkemailcampaign')
        ).order_by('-usage_count')[:5]

        # Get email status breakdown
        status_breakdown = EmailLog.objects.filter(
            user=request.user,
            created_at__date__range=[start_date, end_date]
        ).values('status').annotate(count=Count('status'))

        return Response({
            'date_range': {
                'start_date': start_date,
                'end_date': end_date,
                'days': days
            },
            'summary': {
                'total_emails': total_emails,
                'total_campaigns': total_campaigns,
                'templates_count': EmailTemplate.objects.filter(user=request.user).count()
            },
            'analytics': EmailAnalyticsSerializer(analytics_data, many=True).data,
            'top_templates': [
                {'name': template.name, 'usage_count': template.usage_count}
                for template in top_templates
            ],
            'status_breakdown': list(status_breakdown)
        })


class EmailAnalyticsUpdateView(APIView):
    """Update analytics when emails are sent"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        today = timezone.now().date()
        
        # Get or create today's analytics
        analytics, created = EmailAnalytics.objects.get_or_create(
            user=request.user,
            date=today,
            defaults={
                'emails_sent': 0,
                'unique_recipients': 0,
                'templates_used': 0,
                'campaigns_completed': 0
            }
        )

        # Update counts
        analytics.emails_sent += 1
        analytics.save()

        return Response({'detail': 'Analytics updated'}, status=200)

