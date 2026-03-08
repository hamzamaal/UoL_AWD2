"""ASGI config for the MindLMS project.

This module exposes the ASGI application used by Django Channels for both
standard HTTP requests and WebSocket connections.
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import forum.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MindLMS.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(forum.routing.websocket_urlpatterns)
        ),
    }
)
