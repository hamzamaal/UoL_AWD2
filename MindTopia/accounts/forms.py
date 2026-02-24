from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile


class UserRegisterForm(UserCreationForm):
    """ Custom user registration form with additional fields """
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'role']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            # Create a UserProfile linked to this user
            UserProfile.objects.create(
                user=user,
                first_name=user.first_name,
                last_name=user.last_name,
                role=self.cleaned_data['role']
            )
        return user


class UserUpdateForm(forms.ModelForm):
    """ Form to update user details (username, email, first & last name) """
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    """ Form to update UserProfile details including bio, location, and profile image """
    class Meta:
        model = UserProfile
        fields = ['bio', 'location', 'date_of_birth', 'image']


class StatusUpdateForm(forms.ModelForm):
    """ Form to allow students to post a status update on their profile """
    class Meta:
        model = UserProfile
        fields = ['status_update']
        widgets = {
            'status_update': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'What’s on your mind?'}),
        }
