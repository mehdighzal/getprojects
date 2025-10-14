from django.conf import settings
from django.db import models


class EmailLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    recipients = models.TextField(help_text='Comma-separated emails')
    created_at = models.DateTimeField(auto_now_add=True)


