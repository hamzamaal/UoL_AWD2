"""Database models for the forum app."""

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Post(models.Model):
    """Store a forum discussion post."""

    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Return the post title for human-readable displays."""
        return self.title

    def get_absolute_url(self):
        """Return the URL for this post's detail page."""
        return reverse('post-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    """Store a comment attached to a forum post."""

    post = models.ForeignKey('forum.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    class Meta:
        """Return the newest comments first."""

        ordering = ['-date_posted']

    def approve(self):
        """Mark the current comment as approved."""
        self.approved_comment = True
        self.save()

    def __str__(self):
        """Return the comment content for human-readable displays."""
        return self.content
