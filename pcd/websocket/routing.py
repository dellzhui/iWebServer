from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/api', consumers.PCDConsumer.as_asgi()),
]
