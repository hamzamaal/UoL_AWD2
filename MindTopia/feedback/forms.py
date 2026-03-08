"""Form definitions for the feedback application."""

from django import forms

from .models import Feedback


class FeedbackForm(forms.ModelForm):
    """Form used to collect structured feedback from users."""

    class Meta:
        """Define the Feedback model fields exposed in the form."""

        model = Feedback
        fields = [
            "ui",
            "sug",
            "satisfy",
            "sugg",
            "rating",
        ]