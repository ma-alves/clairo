from chat.consumers import OnlineConsumer, ChatConsumer
from chat.models import Chat

from channels.auth import AuthMiddlewareStack
from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator
from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase
from django.urls import path


class OnlineTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username="usuario_de_teste", password="Senha1234!")
        cls.anom_user = AnonymousUser()
        cls.application = AuthMiddlewareStack(OnlineConsumer.as_asgi())

    async def test_online_connect(self):
        communicator = WebsocketCommunicator(self.application, "/ws/online-status/")
        connected, subprotocol = await communicator.connect()
        assert connected

        await communicator.send_json_to({"type": "open", "user_id": 1})
        response = await communicator.receive_json_from()
        assert response == {"status": True, "user_id": 1}
        
        await communicator.disconnect()

    async def test_online_disconnect(self):
        communicator = WebsocketCommunicator(self.application, "/ws/online-status/")
        await communicator.connect()
        await communicator.send_json_to({"type": "closed", "user_id": 1})
        response = await communicator.receive_json_from()
        assert response == {"status": False, "user_id": 1}
        
        await communicator.disconnect()

    async def test_type_error(self):
        communicator = WebsocketCommunicator(self.application, "/ws/online-status/")
        await communicator.connect()
        await communicator.send_json_to({"type": "not_a_type", "user_id": 1})
        response = await communicator.receive_json_from()
        
        assert response == {"error": "STATUS INVÁLIDO"}
        
        await communicator.disconnect()

    async def test_user_error(self):
        communicator = WebsocketCommunicator(self.application, "/ws/online-status/")
        await communicator.connect()
        await communicator.send_json_to({"type": "open", "user_id": "not_an_int"})
        response = await communicator.receive_json_from()

        assert response == {"error": "ID INVÁLIDO"}
        
        await communicator.disconnect()


class ChatTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="usuario_de_teste1", password="Senha1234!")
        self.user2 = User.objects.create_user(username="usuario_de_teste2", password="Senha1234!")
        self.chat = Chat.objects.create()
        self.chat.users.add(self.user1, self.user2)
        self.application = AuthMiddlewareStack(
            URLRouter([
                path(f"ws/chat/<chat_uuid>/", ChatConsumer.as_asgi()), # type: ignore
            ])
        )

    async def test_chat_connect(self):
        communicator = WebsocketCommunicator(self.application, f"/ws/chat/{self.chat.chat_uuid}/")
        connected, subprotocol = await communicator.connect()
        assert connected

        await communicator.disconnect()

    async def test_chat_message(self):
        communicator = WebsocketCommunicator(self.application, f"/ws/chat/{self.chat.chat_uuid}/")
        communicator.scope["user"] = self.user1  # type: ignore
        await communicator.connect()

        message = {
            "type": "chat.message",
            "message": "teste",
            "user": self.user1.id, # type: ignore
        }
        await communicator.send_json_to(message)
        response = await communicator.receive_json_from()

        assert response.get("message") == "teste"
        assert response.get("user") == self.user1.id  # type: ignore
        assert "time" in response

        await communicator.disconnect()
        