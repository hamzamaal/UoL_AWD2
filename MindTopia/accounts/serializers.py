"""Serializer classes for the accounts app."""

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    """Serialize core fields from Django's built-in User model."""

    class Meta:
        """Define the serialised User fields."""

        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class UserProfileSerializer(serializers.ModelSerializer):
    """Serialize extended profile data together with nested user data."""

    user = UserSerializer(read_only=True)

    class Meta:
        """Define the serialised UserProfile fields."""

        model = UserProfile
        fields = [
            'id',
            'user',
            'role',
            'bio',
            'location',
            'date_of_birth',
            'image',
            'status_update',
        ]
