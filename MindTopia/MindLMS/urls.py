"""MindLMS URL Configuration"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Import views from different apps
from core import views as h
from accounts import views as ac
from courses import views as c
from donate import views as don
from quiz import views as qui
from feedback import views as fee
from instructors import views as inss
from quizapi import views as quiz_views

# Django Authentication Views
from django.contrib.auth import views as auth_views

# Django Rest Framework
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import AllowAny

# Import ASGI application for WebSockets
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import forum.routing


class ApiIndexView(APIView):
    """Browsable API index showing available endpoints"""
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            "MindTopia API": {
                "Public Endpoints": {
                    "Courses": reverse('api_courses', request=request),
                    "Course Detail": request.build_absolute_uri('/api/courses/<id>/'),
                    "Quiz List": reverse('api_quiz_list', request=request),
                    "Quiz Detail": request.build_absolute_uri('/api/quiz/<id>/'),
                    "Course Quiz": request.build_absolute_uri('/api/courses/<course_id>/quiz/')
                },
                "Teacher Only Endpoints": {
                    "Users": reverse('api_users', request=request),
                    "Students": reverse('api_students', request=request),
                    "User Profile": request.build_absolute_uri('/api/user/<username>/'),
                    "Course Feedback": request.build_absolute_uri('/api/courses/<course_id>/feedback/')
                }
            }
        })


urlpatterns = [
    path('admin/', admin.site.urls),

    # Home & General Pages
    path('', h.home, name='home'),
    path('about/', h.about, name='about'),
    path('donate/', don.pay, name='donate'),
    path('instructors/', inss.instruc, name='instructors'),
    path('questions/', qui.qpage, name='questions'),

    # Authentication & User Profiles
    path('register/', ac.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('profile/', ac.profile, name='profile'),
    path('profile_update/', ac.profile_update, name='profile_update'),

    # Courses & Course Details
    path('courses/', c.courses, name='courses'),
    path('course/<int:course_id>/', c.course_detail, name='course_detail'),
    path('course/<int:course_id>/register/', c.register_course, name='register_course'),
    path('course/<int:course_id>/feedback/', c.submit_feedback, name='submit_feedback'),

    # API Index
    path('api/', ApiIndexView.as_view(), name='api_index'),

    # Course API Endpoints
    path('api/courses/', c.CourseListApiView.as_view(), name='api_courses'),
    path('api/courses/<int:pk>/', c.CourseDetailApiView.as_view(), name='api_course_detail'),
    path('api/courses/<int:course_id>/feedback/', c.CourseFeedbackListApiView.as_view(), name='api_course_feedback'),

    # Forum URLs
    path('discussion_forum/', include('forum.urls')),
    path('chat/', include('forum.urls')),

    # Feedback System
    path('feedback/', fee.feed, name='feedback'),

    # Quiz API
    path('api/quiz/', quiz_views.QuizApiList.as_view(), name='api_quiz_list'),
    path('api/quiz/<int:pk>/', quiz_views.QuizApiDetail.as_view(), name='api_quiz_detail'),
    path('api/courses/<int:course_id>/quiz/', quiz_views.QuizByCourseApiList.as_view(), name='api_course_quiz_list'),
    path('quizapi/', quiz_views.QuizApiList.as_view(), name='quizapi_legacy'),

    # Accounts URLs
    path('', include('accounts.urls')),
]

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            forum.routing.websocket_urlpatterns
        )
    ),
})

urlpatterns = format_suffix_patterns(urlpatterns)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)