"""Database models for the instructors app."""

from django.db import models


class Instructor(models.Model):
    """Store instructor details displayed across the platform."""

    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='instruct', default='default.jpg')
    url = models.CharField(max_length=255, default='#')

    def __str__(self):
        """Return the instructor name for human-readable displays."""
        return self.name
