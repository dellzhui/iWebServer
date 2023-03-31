from django.urls import path
from websocket.consumers import iWebServerConsumer

websocket_urlpatterns = [
    path('ws/api', iWebServerConsumer.as_asgi()),
]