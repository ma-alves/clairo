from channels.auth import AuthMiddlewareStack
from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import path

from chat.consumers import ChatConsumer, OnlineConsumer
from chat.models import Chat


class ChatTestCase(TestCase):
	@classmethod
	def setUpTestData(cls):
		cls.user1 = User.objects.create_user(
			username='usuario_de_teste1', password='Senha1234!'
		)
		cls.user2 = User.objects.create_user(
			username='usuario_de_teste2', password='Senha1234!'
		)
		cls.chat = Chat.objects.create()
		cls.chat.users.add(cls.user1, cls.user2)
		cls.application = AuthMiddlewareStack(
			URLRouter(
				[
					path('ws/chat/<chat_uuid>/', ChatConsumer.as_asgi()),  # type: ignore
				]
			)
		)

	async def test_chat_connect(self):
		communicator = WebsocketCommunicator(
			self.application, f'/ws/chat/{self.chat.chat_uuid}/'
		)
		connected, subprotocol = await communicator.connect()
		assert connected

	async def test_chat_message(self):
		communicator = WebsocketCommunicator(
			self.application, f'/ws/chat/{self.chat.chat_uuid}/'
		)
		communicator.scope['user'] = self.user1  # type: ignore
		await communicator.connect()

		message = {
			'type': 'chat.message',
			'message': 'teste',
			'user': self.user1.id,  # type: ignore
		}
		await communicator.send_json_to(message)
		response = await communicator.receive_json_from()

		assert response.get('message') == 'teste'
		assert response.get('user') == self.user1.id  # type: ignore
		assert 'time' in response

		await communicator.disconnect()

	async def test_message_error(self):
		communicator = WebsocketCommunicator(
			self.application, f'/ws/chat/{self.chat.chat_uuid}/'
		)
		communicator.scope['user'] = self.user1  # type: ignore
		await communicator.connect()

		await communicator.send_json_to({'type': 'invalid_message'})
		response = await communicator.receive_json_from()

		assert response == {'error': 'Mensagem Invalida'}


class OnlineTestCase(TestCase):
	@classmethod
	def setUpTestData(cls):
		cls.user1 = User.objects.create_user(username='usuario_de_teste', password='Senha1234!')
		cls.application = AuthMiddlewareStack(OnlineConsumer.as_asgi())

	async def test_online_connect(self):
		communicator = WebsocketCommunicator(self.application, '/ws/online-status/')
		connected, subprotocol = await communicator.connect()
		assert connected

		await communicator.send_json_to({'type': 'open', 'user_id': self.user1.id}) # type: ignore
		response = await communicator.receive_json_from()
		assert response == {'status': True, 'user_id': self.user1.id} # type: ignore

	async def test_online_disconnect(self):
		communicator = WebsocketCommunicator(self.application, '/ws/online-status/')
		await communicator.connect()
		await communicator.send_json_to({'type': 'closed', 'user_id': self.user1.id}) # type: ignore

		response = await communicator.receive_json_from()
		assert response == {'status': False, 'user_id': self.user1.id} # type: ignore

	async def test_type_error(self):
		communicator = WebsocketCommunicator(self.application, '/ws/online-status/')
		await communicator.connect()
		await communicator.send_json_to({'type': 'not_a_type', 'user_id': 1})

		response = await communicator.receive_json_from()
		assert response == {'error': 'Status Invalido'}

		await communicator.disconnect()

	async def test_user_error(self):
		communicator = WebsocketCommunicator(self.application, '/ws/online-status/')
		await communicator.connect()
		await communicator.send_json_to({'type': 'open', 'user_id': 'not_an_int'})

		response = await communicator.receive_json_from()
		assert response == {'error': 'Id Invalido'}

		await communicator.disconnect()
