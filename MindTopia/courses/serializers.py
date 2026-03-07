from rest_framework import serializers
from .models import Course, CourseFeedback


class CourseSerializer(serializers.ModelSerializer):
    instructor_name = serializers.CharField(source='instructor.name', read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'logo', 'instructor', 'instructor_name', 'video', 'pdf', 'url']


class CourseFeedbackSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = CourseFeedback
        fields = ['id', 'course', 'user', 'username', 'comment', 'rating', 'created_at']