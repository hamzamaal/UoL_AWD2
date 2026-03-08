"""Root URL configuration for the MindLMS project."""

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.core.asgi import get_asgi_application
from django.urls import include, path
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.views import APIView

import forum.routing


class ApiIndexView(APIView):
    """Return a browsable index of the available API endpoints."""

    permission_classes = [AllowAny]

    def get(self, request):
        """Return the grouped list of public and teacher-only endpoints."""
        return Response(
            {
                'MindTopia API': {
                    'Public Endpoints': {
                        'Courses': reverse('api_courses', request=request),
                        'Course Detail': request.build_absolute_uri('/api/courses/<id>/'),
                        'Quiz List': reverse('api_quiz_list', request=request),
                        'Quiz Detail': request.build_absolute_uri('/api/quiz/<id>/'),
                        'Course Quiz': request.build_absolute_uri(
                            '/api/courses/<course_id>/quiz/'
                        ),
                    },
                    'Teacher Only Endpoints': {
                        'Users': reverse('api_users', request=request),
                        'Students': reverse('api_students', request=request),
                        'User Profile': request.build_absolute_uri(
                            '/api/user/<username>/'
                        ),
                        'Course Feedback': request.build_absolute_uri(
                            '/api/courses/<course_id>/feedback/'
                        ),
                    },
                }
            }
        )


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', ApiIndexView.as_view(), name='api_index'),
    path('', include('core.urls')),
    path('', include('accounts.urls')),
    path('', include('courses.urls')),
    path('donate/', include('donate.urls')),
    path('instructors/', include('instructors.urls')),
    path('feedback/', include('feedback.urls')),
    path('questions/', include('quiz.urls')),
    path('api/', include('quizapi.urls')),
    path('discussion_forum/', include('forum.urls')),
    path('chat/', include('forum.urls')),
]

application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'websocket': AuthMiddlewareStack(
            URLRouter(forum.routing.websocket_urlpatterns)
        ),
    }
)

urlpatterns = format_suffix_patterns(urlpatterns)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
