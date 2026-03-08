"""Form definitions for the accounts application.

This module contains Django form classes used for user registration,
account updates, profile updates, and status updates.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import transaction

from .models import UserProfile


class UserRegisterForm(UserCreationForm):
    """
    Registration form used to create a new user account.

    Extends Django's built-in UserCreationForm to include additional
    profile information such as email, first name, last name, and role.
    """

    # Additional fields required during registration
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)

    # Role selection stored in the related UserProfile model
    role = forms.ChoiceField(
        choices=UserProfile.ROLE_CHOICES,
        required=True
    )

    class Meta:
        """Define the model and fields used during registration."""
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
            "role",
        ]

    @transaction.atomic
    def save(self, commit=True):
        """
        Create a new user and synchronise the related UserProfile.

        The operation is wrapped in an atomic transaction to ensure
        that both the User and UserProfile records are created
        consistently.
        """
        # Create the user object without saving immediately
        user = super().save(commit=False)

        # Populate additional user fields from the form
        user.first_name = self.cleaned_data.get("first_name", "")
        user.last_name = self.cleaned_data.get("last_name", "")
        user.email = self.cleaned_data.get("email", "")

        if commit:
            # Save the user to the database
            user.save()

            # Ensure a profile exists and update its role
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.role = self.cleaned_data["role"]
            profile.save()

        return user


class UserUpdateForm(forms.ModelForm):
    """
    Form used to update basic account information.

    Edits fields stored on Django's built-in User model.
    """

    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)

    class Meta:
        """Define editable fields for updating account information."""
        model = User
        fields = ["username", "email", "first_name", "last_name"]


class ProfileUpdateForm(forms.ModelForm):
    """
    Form used to update extended profile information.

    These fields are stored in the UserProfile model rather than
    Django's default User model.
    """

    class Meta:
        """Define editable profile fields."""
        model = UserProfile
        fields = ["bio", "location", "date_of_birth", "image"]


class StatusUpdateForm(forms.ModelForm):
    """
    Form allowing users to post a short status message
    displayed on their profile page.
    """

    class Meta:
        """Define the status field and its custom textarea widget."""
        model = UserProfile
        fields = ["status_update"]

        widgets = {
            "status_update": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 2,
                    "placeholder": "What's on your mind?",
                }
            ),
        }