"""Form definitions for the feedback application."""

from django import forms

from .models import Feedback


class FeedbackForm(forms.ModelForm):
    """Model form used to collect structured user feedback."""

    class Meta:
        """Specify the Feedback model fields included in the form."""

        model = Feedback
        fields = ["ui", "sug", "satisfy", "sugg", "rating"]