"""MindLMS URL Configuration"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Import views from different apps
from core import views as h
from accounts import views as ac
from courses import views as c
from forum import views as fr  #  Forum views (Ensure correct import)
from donate import views as don
from quiz import views as qui
from feedback import views as fee
from instructors import views as inss
from quizapi import views as quiz_views

# Django Authentication Views
from django.contrib.auth import views as auth_views

# Django Rest Framework
from rest_framework.urlpatterns import format_suffix_patterns

# Import ASGI application for WebSockets
from django.core.asgi import get_asgi_application  
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import forum.routing  #  WebSocket routing for chat

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
    path('course/<int:course_id>/feedback/', c.submit_feedback, name='submit_feedback'),

    #  Include Forum URLs (Ensures chat URL is accessible)
    path('discussion_forum/', include('forum.urls')),
    path('chat/', include('forum.urls')),  #  Fix for WebSocket chat

    # Feedback System
    path('feedback/', fee.feed, name='feedback'),

    # Quiz API
    path('quizapi/', quiz_views.QuizApiList.as_view()),
    path('', include('accounts.urls')),  # Ensure this line is present

]

#  WebSockets Setup for Django Channels (ASGI)
application = ProtocolTypeRouter({
    "http": get_asgi_application(),  #  Ensures ASGI app runs correctly
    "websocket": AuthMiddlewareStack(
        URLRouter(
            forum.routing.websocket_urlpatterns  #  WebSocket URLs
        )
    ),
})

# Enable format suffixes for DRF API
urlpatterns = format_suffix_patterns(urlpatterns)

#  Serve media & static files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
