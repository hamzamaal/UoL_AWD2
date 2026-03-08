"""ASGI configuration for the MindLMS project.

Exposes the ASGI callable used by Django Channels to handle both HTTP
requests and WebSocket connections.
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application


# Set the Django settings module before importing anything that depends on it.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MindLMS.settings")

# Initialize Django ASGI application early so the app registry is ready
# before importing WebSocket routing and consumers.
django_asgi_app = get_asgi_application()

# Import WebSocket routing only after Django has been initialized.
import forum.routing  # noqa: E402


# Route standard HTTP requests to Django and WebSocket traffic to Channels.
application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AuthMiddlewareStack(
            URLRouter(forum.routing.websocket_urlpatterns)
        ),
    }
)