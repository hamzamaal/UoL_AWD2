from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    """Serializes User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes UserProfile model"""
    user = UserSerializer(read_only=True)  # Nested user data

    class Meta:
        model = UserProfile
        fields = ['user', 'role', 'bio', 'location', 'date_of_birth', 'image']

