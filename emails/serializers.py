from rest_framework import serializers
from .models import EmailLog, EmailTemplate, BulkEmailCampaign, EmailAnalytics


class SendEmailSerializer(serializers.Serializer):
    subject = serializers.CharField(max_length=255)
    body = serializers.CharField()
    recipients = serializers.ListField(
        child=serializers.EmailField(), allow_empty=False
    )


class EmailLogSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    subject = serializers.CharField()
    body = serializers.CharField()
    recipients = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField()
    status = serializers.CharField()
    error_message = serializers.CharField()

    def get_recipients(self, obj):
        return [r.strip() for r in obj.recipients.split(',') if r.strip()]


class EmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTemplate
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']


class BulkEmailCampaignSerializer(serializers.ModelSerializer):
    template_name = serializers.CharField(source='template.name', read_only=True)
    
    class Meta:
        model = BulkEmailCampaign
        fields = '__all__'
        read_only_fields = ['user', 'sent_count', 'created_at', 'started_at', 'completed_at']


class EmailAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailAnalytics
        fields = '__all__'
        read_only_fields = ['user']

