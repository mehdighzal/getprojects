from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

# Register UserProfile as inline with User
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('bio', 'company', 'job_title', 'location', 'phone', 
              'github_url', 'website_url', 'linkedin_url', 'twitter_url', 'work_image')
    readonly_fields = ('created_at', 'updated_at')

# Extend User admin to include profile
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')

# Re-register User admin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register UserProfile separately for direct access
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'job_title', 'location', 'created_at')
    list_filter = ('created_at', 'updated_at', 'company')
    search_fields = ('user__username', 'user__email', 'company', 'job_title', 'location')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Professional Information', {
            'fields': ('company', 'job_title', 'location', 'phone')
        }),
        ('Social Links', {
            'fields': ('github_url', 'website_url', 'linkedin_url', 'twitter_url'),
            'classes': ('collapse',)
        }),
        ('Additional Information', {
            'fields': ('bio', 'work_image'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
