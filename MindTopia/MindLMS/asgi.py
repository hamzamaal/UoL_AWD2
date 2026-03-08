"""ASGI configuration for the MindLMS project.

Exposes the ASGI callable used by Django Channels to handle both HTTP
requests and WebSocket connections.
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import forum.routing


# Set the default Django settings module for the ASGI application.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MindLMS.settings")


# Define the ASGI application handling HTTP and WebSocket protocols.
application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(forum.routing.websocket_urlpatterns)
        ),
    }
)