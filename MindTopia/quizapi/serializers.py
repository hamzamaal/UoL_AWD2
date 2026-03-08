"""Serializer classes for the quiz API application."""

from rest_framework import serializers

from quiz.models import Quiz


class QuizApiSerializer(serializers.ModelSerializer):
    """Serialize quiz questions along with the related course title."""

    # Read-only field exposing the course title from the related model.
    course_title = serializers.CharField(source="course.title", read_only=True)

    class Meta:
        """Define the fields returned by the quiz API serializer."""

        model = Quiz
        fields = [
            "id",
            "course",
            "course_title",
            "question",
            "option1",
            "option2",
            "option3",
            "option4",
            "answer",
        ]