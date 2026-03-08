"""Form definitions for the forum app."""

from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    """Allow users to submit a comment body for a forum post."""

    class Meta:
        """Exclude fields set automatically by the view logic."""

        model = Comment
        exclude = ('author', 'post', 'date_posted', 'approved_comment')
