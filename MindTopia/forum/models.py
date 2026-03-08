"""Database models for the forum application."""

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Post(models.Model):
    """Store a discussion forum post created by a user."""

    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Return the post title for readable representations."""
        return self.title

    def get_absolute_url(self):
        """Return the URL for the post detail page."""
        return reverse("post-detail", kwargs={"pk": self.pk})


class Comment(models.Model):
    """Store a comment attached to a forum post."""

    post = models.ForeignKey(
        Post,
        related_name="comments",
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a short readable representation of the comment."""
        return f"Comment by {self.author.username} on {self.post.title}"


class ChatMessage(models.Model):
    """Store persistent room-based chat messages for WebSocket chat history."""

    room_name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Define default ordering for chat history retrieval."""

        ordering = ["timestamp"]

    def __str__(self):
        """Return a readable representation of the chat message."""
        return f"{self.user.username} in {self.room_name}: {self.message[:30]}"