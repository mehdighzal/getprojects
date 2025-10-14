from rest_framework import serializers


class SendEmailSerializer(serializers.Serializer):
    subject = serializers.CharField(max_length=255)
    body = serializers.CharField()
    recipients = serializers.ListField(
        child=serializers.EmailField(), allow_empty=False
    )


