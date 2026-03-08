"""APIView classes for quiz-related API endpoints."""

from rest_framework import generics
from rest_framework.permissions import AllowAny

from quiz.models import Quiz

from .serializers import QuizApiSerializer


class QuizApiList(generics.ListAPIView):
    """Return the public list of all quiz questions."""

    queryset = Quiz.objects.all().order_by('id')
    serializer_class = QuizApiSerializer
    permission_classes = [AllowAny]


class QuizApiDetail(generics.RetrieveAPIView):
    """Return the public API detail view for one quiz question."""

    queryset = Quiz.objects.all()
    serializer_class = QuizApiSerializer
    permission_classes = [AllowAny]


class QuizByCourseApiList(generics.ListAPIView):
    """Return public quiz questions filtered to a single course."""

    serializer_class = QuizApiSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """Filter quiz questions to the course referenced in the URL."""
        return Quiz.objects.filter(course_id=self.kwargs['course_id']).order_by('id')
