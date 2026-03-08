"""Database models for the accounts app."""

from django.contrib.auth.models import User
from django.db import models
from PIL import Image

from courses.models import Course


class UserProfile(models.Model):
    """Extend the built-in User model with application-specific fields."""

    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='userprofile',
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    bio = models.TextField(max_length=500, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    status_update = models.TextField(
        blank=True,
        null=True,
        help_text='Share your latest update!',
    )
    registered_courses = models.ManyToManyField(
        Course,
        blank=True,
        related_name='students',
    )
    students = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank=True,
        related_name='teacher_students',
    )

    def __str__(self):
        """Return a readable representation of the profile record."""
        return f'{self.user.username} - {self.get_role_display()}'

    def save(self, *args, **kwargs):
        """Save the profile and resize large uploaded images."""
        super().save(*args, **kwargs)

        if not self.image or not hasattr(self.image, 'path'):
            return

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            img.thumbnail((300, 300))
            img.save(self.image.path)
