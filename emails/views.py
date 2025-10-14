from django.core.mail import send_mail
from django.conf import settings
import os
import base64
import smtplib
from email.mime.text import MIMEText
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import SendEmailSerializer, EmailLogSerializer
from .models import EmailLog


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

