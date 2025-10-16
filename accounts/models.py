from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import os


def user_profile_image_path(instance, filename):
    """Generate upload path for user profile images."""
    ext = filename.split('.')[-1]
    filename = f"profile_{instance.user.id}.{ext}"
    return os.path.join('profile_images', filename)


class UserProfile(models.Model):
    """Extended user profile with additional fields."""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True, null=True)
    github_url = models.URLField(max_length=200, blank=True, null=True)
    website_url = models.URLField(max_length=200, blank=True, null=True)
    linkedin_url = models.URLField(max_length=200, blank=True, null=True)
    twitter_url = models.URLField(max_length=200, blank=True, null=True)
    work_image = models.ImageField(upload_to=user_profile_image_path, blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    @property
    def full_name(self):
        """Return user's full name."""
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        return self.user.username
