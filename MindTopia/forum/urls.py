from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    chat_room
)
from . import views  # Import views for function-based views

urlpatterns = [
    # Forum post-related URLs
    path('', PostListView.as_view(), name='forum'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),

    # Chat room URL (Fixed Duplicate Definitions)
    path('chat/<str:room_name>/', chat_room, name='chat_room'),
]
