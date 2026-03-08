"""Serializer classes for the quiz API app."""

from rest_framework import serializers

from quiz.models import Quiz


class QuizApiSerializer(serializers.ModelSerializer):
    """Serialize quiz questions together with the related course title."""

    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        """Define the quiz fields returned by the API."""

        model = Quiz
        fields = [
            'id',
            'course',
            'course_title',
            'question',
            'option1',
            'option2',
            'option3',
            'option4',
            'answer',
        ]
