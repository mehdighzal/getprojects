from django.contrib import admin
from .models import AIRequest

@admin.register(AIRequest)
class AIRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'request_type', 'status', 'created_at')
    list_filter = ('request_type', 'status', 'created_at', 'user')
    search_fields = ('user__username', 'request_type', 'response_data')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Request Information', {
            'fields': ('user', 'request_type', 'status')
        }),
        ('Data', {
            'fields': ('request_data', 'response_data'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
