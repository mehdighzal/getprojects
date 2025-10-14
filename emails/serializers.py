from rest_framework import serializers


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

    def get_recipients(self, obj):
        return [r.strip() for r in obj.recipients.split(',') if r.strip()]

