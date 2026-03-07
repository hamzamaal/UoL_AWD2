# Import Django's form utilities used to create and manage form classes
from django import forms

# Import the built-in User model used for authentication and user management
from django.contrib.auth.models import User

# Import Django's default user creation form which includes password validation
from django.contrib.auth.forms import UserCreationForm

# Import the custom UserProfile model from the current application
from .models import UserProfile

# Import transaction management to ensure database operations occur atomically
from django.db import transaction


# Form used to register new users with additional profile information
class UserRegisterForm(UserCreationForm):

    """ Custom user registration form with additional fields """

    # Require users to provide an email address during registration
    email = forms.EmailField(required=True)

    # Field to capture the user's first name
    first_name = forms.CharField(max_length=50, required=True)

    # Field to capture the user's last name
    last_name = forms.CharField(max_length=50, required=True)

    # Field allowing the user to select their role (student or teacher)
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES, required=True)

    # Meta class defines the model and fields used in the form
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'role']

    # Ensure the entire save process is executed as a single database transaction
    @transaction.atomic
    def save(self, commit=True):

        # Create a User object but delay saving to the database
        user = super().save(commit=False)

        # Assign first and last name values from the cleaned form data
        user.first_name = self.cleaned_data.get("first_name", "")
        user.last_name = self.cleaned_data.get("last_name", "")
        user.email = self.cleaned_data.get("email", "")

        # Save the user object if commit is True
        if commit:
            user.save()

            # Retrieve or create the associated UserProfile to avoid duplicates if signals already created one
            profile, _ = UserProfile.objects.get_or_create(user=user)

            # Assign the selected role to the profile
            profile.role = self.cleaned_data["role"]

            # Save the updated profile to the database
            profile.save()

        # Return the created user instance
        return user


# Form used to update basic user account details
class UserUpdateForm(forms.ModelForm):

    """ Form to update user details (username, email, first & last name) """

    # Email field required for updating user information
    email = forms.EmailField(required=True)

    # First name field required for user profile updates
    first_name = forms.CharField(max_length=50, required=True)

    # Last name field required for user profile updates
    last_name = forms.CharField(max_length=50, required=True)

    # Meta class specifying the model and fields included in the form
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


# Form used to update extended user profile information
class ProfileUpdateForm(forms.ModelForm):

    """ Form to update UserProfile details including bio, location, and profile image """

    # Meta class linking the form to the UserProfile model
    class Meta:
        model = UserProfile

        # Fields available for editing within the profile update form
        fields = ['bio', 'location', 'date_of_birth', 'image']


# Form allowing students to post short status updates to their profile
class StatusUpdateForm(forms.ModelForm):

    """ Form to allow students to post a status update on their profile """

    # Meta class linking the form to the UserProfile model
    class Meta:
        model = UserProfile

        # Field used to capture the status update text
        fields = ['status_update']

        # Custom widget used to display the status field as a styled textarea
        widgets = {
            'status_update': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'What’s on your mind?'}),
        }
        