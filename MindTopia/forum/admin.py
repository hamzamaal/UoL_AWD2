"""Admin configuration for the forum application."""

from django.contrib import admin

from .models import ChatMessage, Comment, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Configure how forum posts appear in the admin site."""

    list_display = ("title", "author", "date_posted")
    search_fields = ("title", "content", "author__username")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Configure how comments appear in the admin site."""

    list_display = ("post", "author", "date_posted")
    search_fields = ("content", "author__username", "post__title")


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    """Configure how chat history appears in the admin site."""

    list_display = ("room_name", "user", "timestamp")
    search_fields = ("room_name", "user__username", "message")
    list_filter = ("room_name", "timestamp")