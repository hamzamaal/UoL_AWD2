"""Database models for the quiz app."""

from django.db import models

from courses.models import Course


class Quiz(models.Model):
    """Store a multiple-choice quiz question for a course."""

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='quiz_questions',
        null=True,
        blank=True,
    )
    question = models.CharField(max_length=500)
    option1 = models.CharField(max_length=20)
    option2 = models.CharField(max_length=20)
    option3 = models.CharField(max_length=20)
    option4 = models.CharField(max_length=20)
    answer = models.CharField(max_length=20)

    def __str__(self):
        """Return the question text for human-readable displays."""
        return self.question
