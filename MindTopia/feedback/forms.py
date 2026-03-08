"""Form definitions for the feedback app."""

from django import forms

from .models import Feedback


class FeedbackForm(forms.ModelForm):
    """Collect structured website and course feedback from a user."""

    class Meta:
        """Define the fields exposed to the feedback form."""

        model = Feedback
        fields = ['ui', 'sug', 'satisfy', 'sugg', 'rating']
