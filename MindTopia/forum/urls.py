"""URL routes for the forum application."""

from django.urls import path

from .views import (
    PostCreateView,
    PostDeleteView,
    PostDetailView,
    PostListView,
    PostUpdateView,
    add_comment_to_post,
    chat_room,
)


urlpatterns = [
    path("", PostListView.as_view(), name="forum"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("post/new/", PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
    path(
        "post/<int:pk>/comment/",
        add_comment_to_post,
        name="add_comment_to_post",
    ),
    path("chat/<str:room_name>/", chat_room, name="chat_room"),
]