"""Database models for the feedback application."""

from django.contrib.auth.models import User
from django.db import models


class Feedback(models.Model):
    """Store structured website and course feedback submitted by users."""

    YES_NO_CHOICES = (
        ("y", "Yes"),
        ("n", "No"),
    )

    RATING_CHOICES = (
        ("a", "1"),
        ("b", "2"),
        ("c", "3"),
        ("d", "4"),
        ("e", "5"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    ui = models.CharField(
        "Did you like the UI of our website?",
        max_length=30,
        choices=YES_NO_CHOICES,
    )

    sug = models.TextField(
        "Suggest some changes to the website",
        default="",
    )

    satisfy = models.CharField(
        "Are you satisfied with course content?",
        max_length=30,
        choices=YES_NO_CHOICES,
    )

    sugg = models.TextField(
        "Suggest changes in course content or possible additions",
        default="",
    )

    rating = models.CharField(
        "Rate your experience",
        max_length=10,
        choices=RATING_CHOICES,
    )

    def __str__(self):
        """Return the username if available, otherwise label as anonymous."""
        return self.user.username if self.user else "Anonymous Feedback"