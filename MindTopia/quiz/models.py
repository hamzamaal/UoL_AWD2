"""Database models for the quiz application."""

from django.db import models

from courses.models import Course


class Quiz(models.Model):
    """Represent a multiple-choice quiz question linked to a course."""

    # Optional relationship allowing a quiz question to belong to a course.
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="quiz_questions",
        null=True,
        blank=True,
    )

    question = models.CharField(max_length=500)

    # Multiple-choice answer options.
    option1 = models.CharField(max_length=20)
    option2 = models.CharField(max_length=20)
    option3 = models.CharField(max_length=20)
    option4 = models.CharField(max_length=20)

    # Correct answer corresponding to one of the options.
    answer = models.CharField(max_length=20)

    def __str__(self):
        """Return the question text for readable representations."""
        return self.question