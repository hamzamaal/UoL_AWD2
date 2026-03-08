"""Serializer classes for the courses app."""

from rest_framework import serializers

from .models import Course, CourseFeedback


class CourseSerializer(serializers.ModelSerializer):
    """Serialize public course information for API responses."""

    instructor_name = serializers.CharField(source='instructor.name', read_only=True)

    class Meta:
        """Define the course fields returned by the API."""

        model = Course
        fields = [
            'id',
            'title',
            'description',
            'logo',
            'instructor',
            'instructor_name',
            'video',
            'pdf',
            'url',
        ]


class CourseFeedbackSerializer(serializers.ModelSerializer):
    """Serialize course feedback data for teacher-facing API responses."""

    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        """Define the feedback fields returned by the API."""

        model = CourseFeedback
        fields = ['id', 'course', 'user', 'username', 'comment', 'rating', 'created_at']
