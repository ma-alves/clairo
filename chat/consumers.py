import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from chat.models import Chat, ChatMessage


class ChatConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def create_message(self, chat_uuid, author, body_message):
        chat = Chat.objects.get(chat_uuid=chat_uuid)
        return ChatMessage.objects.create(
            chat = chat,
            author = author,
            body = body_message
        )
    
    async def connect(self):
        self.user = self.scope["user"] # type: ignore
        self.room_name = self.scope["url_route"]["kwargs"]["chat_uuid"] # type: ignore
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )

        await self.accept()


    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body_message = text_data_json["message"]

        await self.create_message(self.room_name, self.user, body_message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "chat.message",
                "message": body_message,
                "user": self.user.id # type: ignore
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        user = event["user"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "message": message,
            "user": user
        })
        )