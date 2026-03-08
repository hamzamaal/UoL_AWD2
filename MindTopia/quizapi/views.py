"""APIView classes for quiz-related API endpoints."""

from rest_framework import generics
from rest_framework.permissions import AllowAny

from quiz.models import Quiz

from .serializers import QuizApiSerializer


class QuizApiList(generics.ListAPIView):
    """Return a public list of all quiz questions."""

    # Base queryset ordered for consistent API responses.
    queryset = Quiz.objects.all().order_by("id")
    serializer_class = QuizApiSerializer
    permission_classes = [AllowAny]


class QuizApiDetail(generics.RetrieveAPIView):
    """Return the API detail view for a single quiz question."""

    queryset = Quiz.objects.all()
    serializer_class = QuizApiSerializer
    permission_classes = [AllowAny]


class QuizByCourseApiList(generics.ListAPIView):
    """Return quiz questions filtered by course."""

    serializer_class = QuizApiSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """Return quiz questions belonging to the course in the URL."""
        return Quiz.objects.filter(
            course_id=self.kwargs["course_id"]
        ).order_by("id")