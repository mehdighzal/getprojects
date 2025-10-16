from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile extended fields."""
    work_image = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = [
            'bio', 'github_url', 'website_url', 'linkedin_url', 'twitter_url',
            'work_image', 'company', 'job_title', 'location', 'phone',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_work_image(self, obj):
        """Return full URL for work image."""
        if obj.work_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.work_image.url)
            return obj.work_image.url
        return None


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user profile data."""
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'last_login', 'profile']
        read_only_fields = ['id', 'date_joined', 'last_login']


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile."""
    profile = UserProfileSerializer(required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'profile']
    
    def validate_username(self, value):
        """Ensure username is unique (excluding current user)."""
        user = self.context['request'].user
        if User.objects.filter(username=value).exclude(id=user.id).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value
    
    def validate_email(self, value):
        """Ensure email is unique (excluding current user)."""
        user = self.context['request'].user
        if User.objects.filter(email=value).exclude(id=user.id).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    
    def update(self, instance, validated_data):
        """Update user and profile data."""
        print(f"DEBUG: Updating user {instance.username}")
        print(f"DEBUG: Validated data: {validated_data}")
        
        profile_data = validated_data.pop('profile', None)
        print(f"DEBUG: Profile data: {profile_data}")
        
        # Update user fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        print(f"DEBUG: User fields updated")
        
        # Update or create profile
        if profile_data:
            profile, created = UserProfile.objects.get_or_create(user=instance)
            print(f"DEBUG: Profile {'created' if created else 'found'}")
            for attr, value in profile_data.items():
                print(f"DEBUG: Setting profile.{attr} = {value}")
                setattr(profile, attr, value)
            profile.save()
            print(f"DEBUG: Profile saved")
        else:
            print("DEBUG: No profile data to update")
        
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing user password."""
    
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
    confirm_password = serializers.CharField(required=True)
    
    def validate(self, data):
        """Validate that new passwords match."""
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("New passwords do not match.")
        return data
    
    def validate_current_password(self, value):
        """Validate current password."""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect.")
        return value