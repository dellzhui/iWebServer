from django.urls import path
from websocket.consumers import xChatConsumer

websocket_urlpatterns = [
    path('ws/api', xChatConsumer.as_asgi()),
]