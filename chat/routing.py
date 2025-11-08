from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("ws/chat/<chat_uuid>/", consumers.ChatConsumer.as_asgi()), #type: ignore
    path("ws/online-status/", consumers.OnlineConsumer.as_asgi()), #type: ignore
]
