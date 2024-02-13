"""
ASGI config for kernel project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""
from channels.auth import AuthMiddlewareStack
import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path
from client.consumers import *
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kernel.settings')


application = get_asgi_application()

ws_patterns = [
    path('ws/test/', TestConsumer)
]

application = ProtocolTypeRouter({
    "websocket": URLRouter(ws_patterns)# Use TestConsumer.as_asgi() for ASGI compatibility
 
    })

