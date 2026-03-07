from rest_framework import serializers
from quiz.models import Quiz


class QuizApiSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'course', 'course_title', 'question', 'option1', 'option2', 'option3', 'option4', 'answer']