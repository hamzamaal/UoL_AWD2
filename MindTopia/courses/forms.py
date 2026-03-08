"""Form definitions for the courses application."""

from django import forms

from .models import CourseFeedback


class CourseFeedbackForm(forms.ModelForm):
    """Form used to submit feedback and ratings for a course."""

    class Meta:
        """Specify the model fields and form widgets."""

        model = CourseFeedback
        fields = ["comment", "rating"]

        widgets = {
            "comment": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Write your feedback...",
                }
            ),
            "rating": forms.Select(
                choices=[(i, i) for i in range(1, 6)],
                attrs={"class": "form-select"},
            ),
        }
        