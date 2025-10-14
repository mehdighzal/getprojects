from rest_framework import serializers
from .models import Business


class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = [
            'id', 'name', 'email', 'phone', 'website', 'category',
            'country', 'city', 'address', 'created_at',
        ]


