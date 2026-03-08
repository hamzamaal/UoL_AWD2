"""Database models for the instructors application."""

from django.db import models


class Instructor(models.Model):
    """Store instructor information displayed across the platform."""

    name = models.CharField(max_length=50)

    image = models.ImageField(
        upload_to="instruct",
        default="default.jpg",
    )

    url = models.CharField(
        max_length=255,
        default="#",
    )

    def __str__(self):
        """Return the instructor name for display in admin and queries."""
        return self.name