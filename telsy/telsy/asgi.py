'''
Fundación Cardiovascular de Colombia
Dirección de Innovación y Desarrollo Tecnológico
Proyecto Telsy
Telsy Hogar v15.12.2022
Ing. Elmer Rocha Jaime

ASGI config for telsy project.

It exposes the ASGI callable as a module-level variable named "application".
'''

from os import environ
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from monitor.routing import websocket_urlpatterns

environ.setdefault('DJANGO_SETTINGS_MODULE', 'telsy.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
})
