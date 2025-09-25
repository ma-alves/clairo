from django.urls import path

from . import consumers

websocket_urlpatterns = [
    # re_path() não funciona, mas deixar exemplo
    # re_path(r"ws/chat/(?P<chat_uuid>\w+)/$", consumers.ChatConsumer.as_asgi()),
    path("ws/chat/<chat_uuid>/", consumers.ChatConsumer.as_asgi()),
]
