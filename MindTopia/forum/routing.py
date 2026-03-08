"""WebSocket routing for the forum chat feature."""

from django.urls import path

from .consumers import ChatConsumer


# WebSocket URL patterns used by Django Channels.
# The room name is passed to the consumer through the URL.
websocket_urlpatterns = [
    path("ws/chat/<str:room_name>/", ChatConsumer.as_asgi()),
]