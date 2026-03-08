"""Serializer classes for the courses application."""

from rest_framework import serializers

from .models import Course, CourseFeedback


class CourseSerializer(serializers.ModelSerializer):
    """Serialize course data for API responses."""

    instructor_name = serializers.CharField(
        source="instructor.name",
        read_only=True,
    )

    class Meta:
        """Define the fields included in the course API output."""

        model = Course
        fields = [
            "id",
            "title",
            "description",
            "logo",
            "instructor",
            "instructor_name",
            "video",
            "pdf",
            "url",
        ]


class CourseFeedbackSerializer(serializers.ModelSerializer):
    """Serialize feedback data associated with a course."""

    username = serializers.CharField(
        source="user.username",
        read_only=True,
    )

    class Meta:
        """Define the fields included in the feedback API output."""

        model = CourseFeedback
        fields = [
            "id",
            "course",
            "user",
            "username",
            "comment",
            "rating",
            "created_at",
        ]