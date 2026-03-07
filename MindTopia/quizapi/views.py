from rest_framework import generics
from rest_framework.permissions import AllowAny
from quiz.models import Quiz
from .serializers import QuizApiSerializer


# Public API endpoint
class QuizApiList(generics.ListAPIView):
    """Returns all quiz questions (Public)"""
    queryset = Quiz.objects.all().order_by('id')
    serializer_class = QuizApiSerializer
    permission_classes = [AllowAny]


# Public API endpoint
class QuizApiDetail(generics.RetrieveAPIView):
    """Returns one quiz question by primary key (Public)"""
    queryset = Quiz.objects.all()
    serializer_class = QuizApiSerializer
    permission_classes = [AllowAny]


# Public API endpoint
class QuizByCourseApiList(generics.ListAPIView):
    """Returns quiz questions for one course (Public)"""
    serializer_class = QuizApiSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Quiz.objects.filter(course_id=self.kwargs['course_id']).order_by('id')