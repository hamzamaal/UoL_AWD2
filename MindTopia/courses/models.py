"""Database models for the courses app."""

from django.contrib.auth.models import User
from django.db import models

from instructors.models import Instructor


class Course(models.Model):
    """Store the core details and resources for a learning course."""

    title = models.CharField(max_length=255)
    description = models.TextField(default='insert')
    logo = models.ImageField(upload_to='course', default='default.jpg', blank=True)
    instructor = models.ForeignKey(
        Instructor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses',
    )
    video = models.FileField(upload_to='course', null=True, blank=True)
    pdf = models.FileField(upload_to='course', null=True, blank=True)
    url = models.CharField(max_length=255, default='#')

    def __str__(self):
        """Return the course title for human-readable displays."""
        return self.title


class CourseFeedback(models.Model):
    """Store a learner's feedback entry for a course."""

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='feedback')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a readable description of the feedback entry."""
        return f'Feedback by {self.user.username} on {self.course.title}'
