from django.db import models
from django.contrib.auth.models import User

class EmailLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    recipients = models.TextField(help_text='Comma-separated emails')  # Keep original format
    created_at = models.DateTimeField(auto_now_add=True)  # Keep original field name
    status = models.CharField(max_length=20, default='sent')  # sent, failed, pending
    error_message = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.subject} to {len(self.recipients)} recipients"

class EmailTemplate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    category = models.CharField(max_length=50, default='general')  # general, follow-up, introduction, etc.
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'name']

    def __str__(self):
        return self.name

class BulkEmailCampaign(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    template = models.ForeignKey(EmailTemplate, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    recipients = models.JSONField()  # List of business data
    status = models.CharField(max_length=20, default='draft')  # draft, sending, completed, failed
    sent_count = models.IntegerField(default=0)
    total_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.status})"

class EmailAnalytics(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    emails_sent = models.IntegerField(default=0)
    unique_recipients = models.IntegerField(default=0)
    templates_used = models.IntegerField(default=0)
    campaigns_completed = models.IntegerField(default=0)

    class Meta:
        unique_together = ['user', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.date}: {self.emails_sent} emails"