from django.contrib import admin
from .models import Business

@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'phone', 'website', 'category', 'city', 'country', 'created_at')
    list_filter = ('created_at', 'category', 'country', 'city')
    search_fields = ('name', 'address', 'phone', 'website', 'email')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Business Information', {
            'fields': ('name', 'email', 'phone', 'website', 'category')
        }),
        ('Location', {
            'fields': ('address', 'city', 'country'),
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )