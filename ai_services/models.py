from django.db import models
from django.contrib.auth.models import User


class AIRequest(models.Model):
    """Model to track AI service requests and responses."""
    
    REQUEST_TYPES = [
        ('email_generation', 'Email Generation'),
        ('bulk_email', 'Bulk Email Template'),
        ('business_search', 'Business Search'),
        ('gemini_test', 'Gemini Test'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        help_text="User who made the request (null for anonymous requests)"
    )
    request_type = models.CharField(
        max_length=50, 
        choices=REQUEST_TYPES,
        help_text="Type of AI request made"
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending',
        help_text="Current status of the request"
    )
    request_data = models.JSONField(
        default=dict, 
        blank=True,
        help_text="Input data for the AI request"
    )
    response_data = models.JSONField(
        default=dict, 
        blank=True,
        help_text="Response data from the AI service"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'AI Request'
        verbose_name_plural = 'AI Requests'
    
    def __str__(self):
        user_info = self.user.username if self.user else 'Anonymous'
        return f"{user_info} - {self.get_request_type_display()} ({self.status})"
