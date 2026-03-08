"""Form definitions for the accounts app."""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import transaction

from .models import UserProfile


class UserRegisterForm(UserCreationForm):
    """Create a new user account together with its profile data."""

    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES, required=True)

    class Meta:
        """Define the model and fields used during registration."""

        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
            'role',
        ]

    @transaction.atomic
    def save(self, commit=True):
        """Create the user and synchronise the linked profile record."""
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        user.email = self.cleaned_data.get('email', '')

        if commit:
            user.save()
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.role = self.cleaned_data['role']
            profile.save()

        return user


class UserUpdateForm(forms.ModelForm):
    """Update core details stored on Django's built-in User model."""

    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)

    class Meta:
        """Define the editable account fields."""

        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    """Update extended profile information stored on UserProfile."""

    class Meta:
        """Define the editable profile fields."""

        model = UserProfile
        fields = ['bio', 'location', 'date_of_birth', 'image']


class StatusUpdateForm(forms.ModelForm):
    """Allow users to publish a short profile status update."""

    class Meta:
        """Define the status field and its textarea widget."""

        model = UserProfile
        fields = ['status_update']
        widgets = {
            'status_update': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 2,
                    'placeholder': "What's on your mind?",
                }
            ),
        }
