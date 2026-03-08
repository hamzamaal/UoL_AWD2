"""Serializer classes for the accounts application."""

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    """Serialize basic fields from Django's built-in User model."""

    class Meta:
        """Specify the model and fields exposed in the API."""
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serialize extended user profile data.

    Includes nested user information from the related User model.
    """

    # Nested serializer to include basic user account data
    user = UserSerializer(read_only=True)

    class Meta:
        """Specify the model and fields exposed for user profiles."""
        model = UserProfile
        fields = [
            "id",
            "user",
            "role",
            "bio",
            "location",
            "date_of_birth",
            "image",
            "status_update",
        ]