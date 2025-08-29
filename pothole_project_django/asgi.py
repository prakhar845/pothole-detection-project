import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import detector.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pothole_project_django.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            detector.routing.websocket_urlpatterns
        )
    ),
})