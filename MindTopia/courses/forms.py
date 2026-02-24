from django import forms
from .models import CourseFeedback

class CourseFeedbackForm(forms.ModelForm):
    """ Form for students to leave feedback on a course """
    class Meta:
        model = CourseFeedback
        fields = ['comment', 'rating']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write your feedback...'}),
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)], attrs={'class': 'form-select'}),
        }
