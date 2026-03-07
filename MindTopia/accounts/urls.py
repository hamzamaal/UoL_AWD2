from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # User Registration & Authentication
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),

    # User Profile & Home Pages
    path('profile/', views.profile, name='profile'),
    path('profile_update/', views.profile_update, name='profile_update'),
    path('user_home/', views.user_home, name='user_home'),
    path('user_home/<str:username>/', views.user_home, name='user_home_username'),

    # Teacher-Specific Features
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),

    # User API Endpoints
    path('api/users/', views.UserListView.as_view(), name='api_users'),
    path('api/students/', views.StudentListView.as_view(), name='api_students'),
    path('api/user/<str:username>/', views.UserProfileDetailView.as_view(), name='api_user_profile'),
]