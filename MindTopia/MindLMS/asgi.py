import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import forum.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MindLMS.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            forum.routing.websocket_urlpatterns  #WebSocket Routing
        )
    ),
})
