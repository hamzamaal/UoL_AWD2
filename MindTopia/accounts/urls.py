"""URL routes for the accounts app."""

from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile_update/', views.profile_update, name='profile_update'),
    path('user_home/', views.user_home, name='user_home'),
    path('user_home/<str:username>/', views.user_home, name='user_home_username'),
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('api/users/', views.UserListView.as_view(), name='api_users'),
    path('api/students/', views.StudentListView.as_view(), name='api_students'),
    path('api/user/<str:username>/', views.UserProfileDetailView.as_view(), name='api_user_profile'),
]
