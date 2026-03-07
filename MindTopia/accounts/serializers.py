# Import serializer utilities from Django REST Framework
from rest_framework import serializers

# Import Django's built-in User model
from django.contrib.auth.models import User

# Import the UserProfile model from the current app
from .models import UserProfile


# Serializer used to convert User model data into JSON format
class UserSerializer(serializers.ModelSerializer):
    """Serializes User model"""

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


# Serializer used to convert UserProfile model data into JSON format
class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes UserProfile model"""

    # Include nested serialized user data within the profile
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'role', 'bio', 'location', 'date_of_birth', 'image', 'status_update']