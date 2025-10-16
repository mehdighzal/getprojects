from django.contrib import admin
from .models import EmailLog, EmailTemplate, BulkEmailCampaign, EmailAnalytics

@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'subject', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'user')
    search_fields = ('recipients', 'subject', 'user__username')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Email Information', {
            'fields': ('user', 'recipients', 'subject', 'body')
        }),
        ('Status & Tracking', {
            'fields': ('status', 'error_message')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'subject', 'is_default', 'category', 'created_at')
    list_filter = ('is_default', 'category', 'created_at', 'user')
    search_fields = ('name', 'subject', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Template Information', {
            'fields': ('name', 'user', 'subject', 'body', 'category', 'is_default')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(BulkEmailCampaign)
class BulkEmailCampaignAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'status', 'total_count', 'sent_count', 'created_at')
    list_filter = ('status', 'created_at', 'user')
    search_fields = ('name', 'user__username')
    readonly_fields = ('created_at', 'sent_count')
    
    fieldsets = (
        ('Campaign Information', {
            'fields': ('name', 'user', 'template', 'status')
        }),
        ('Recipients', {
            'fields': ('recipients', 'total_count', 'sent_count')
        }),
        ('Timing', {
            'fields': ('started_at', 'completed_at'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(EmailAnalytics)
class EmailAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date', 'emails_sent', 'unique_recipients', 'templates_used', 'campaigns_completed')
    list_filter = ('date', 'user')
    search_fields = ('user__username',)
    readonly_fields = ()
    ordering = ('-date',)
    
    fieldsets = (
        ('Analytics Information', {
            'fields': ('user', 'date', 'emails_sent', 'unique_recipients', 'templates_used', 'campaigns_completed')
        }),
    )
