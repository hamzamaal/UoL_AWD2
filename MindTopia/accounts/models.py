"""Database models for the accounts application.

This module defines the UserProfile model, which extends Django's
built-in User model with application-specific profile data.
"""

from django.contrib.auth.models import User
from django.db import models
from PIL import Image

from courses.models import Course


class UserProfile(models.Model):
    """
    Extend Django's built-in User model with profile information.

    This model stores additional user data such as role, biography,
    location, date of birth, profile image, status updates, and
    course registrations.
    """

    # Available roles used throughout the application.
    ROLE_CHOICES = (
        ("student", "Student"),
        ("teacher", "Teacher"),
    )

    # Link each profile to exactly one Django User account.
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="userprofile",
    )

    # Role used for access control and dashboard behaviour.
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default="student",
    )

    # Optional personal profile fields.
    bio = models.TextField(max_length=500, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    # Uploaded profile image with a default fallback image.
    image = models.ImageField(
        default="default.jpg",
        upload_to="profile_pics",
    )

    # Optional short status message shown on the user's profile page.
    status_update = models.TextField(
        blank=True,
        null=True,
        help_text="Share your latest update!",
    )

    # Courses that a student has registered for.
    registered_courses = models.ManyToManyField(
        Course,
        blank=True,
        related_name="students",
    )

    # Self-referential relationship allowing teachers to be linked
    # to multiple student profiles.
    students = models.ManyToManyField(
        "self",
        symmetrical=False,
        blank=True,
        related_name="teacher_students",
    )

    def __str__(self):
        """Return a human-readable representation of the profile."""
        return f"{self.user.username} - {self.get_role_display()}"

    def save(self, *args, **kwargs):
        """
        Save the profile and resize large uploaded images.

        The image is resized after saving to reduce storage usage and
        keep profile pictures within a consistent maximum dimension.
        """
        super().save(*args, **kwargs)

        # Exit early if no image file is available on disk.
        if not self.image or not hasattr(self.image, "path"):
            return

        img = Image.open(self.image.path)

        # Resize images larger than 300x300 pixels.
        if img.height > 300 or img.width > 300:
            img.thumbnail((300, 300))
            img.save(self.image.path)