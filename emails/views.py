from django.core.mail import send_mail
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import SendEmailSerializer
from .models import EmailLog


class SendEmailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = SendEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        subject = serializer.validated_data['subject']
        body = serializer.validated_data['body']
        recipients = serializer.validated_data['recipients']

        # Send via configured backend (console by default)
        send_mail(subject, body, None, recipients, fail_silently=False)

        EmailLog.objects.create(
            user=request.user,
            subject=subject,
            body=body,
            recipients=','.join(recipients),
        )

        return Response({'sent': len(recipients)}, status=status.HTTP_200_OK)


