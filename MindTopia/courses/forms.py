"""Form definitions for the courses app."""

from django import forms

from .models import CourseFeedback


class CourseFeedbackForm(forms.ModelForm):
    """Collect student feedback for a course."""

    class Meta:
        """Define the feedback fields and Bootstrap-friendly widgets."""

        model = CourseFeedback
        fields = ['comment', 'rating']
        widgets = {
            'comment': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Write your feedback...',
                }
            ),
            'rating': forms.Select(
                choices=[(i, i) for i in range(1, 6)],
                attrs={'class': 'form-select'},
            ),
        }
