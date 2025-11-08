from datetime import datetime
import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from chat.models import Chat, ChatMessage, UserOnlineStatus


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"] # type: ignore
        self.room_name = self.scope["url_route"]["kwargs"]["chat_uuid"] # type: ignore
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    # Receive message from Client
    # recebe a mensagem do cliente, processa o que for e aí sim entrega pro grupo
    # chatSocket.send()
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body_message = text_data_json["message"]

        await self.create_message(self.room_name, self.user, body_message)
        # Send the message that came from the client to room group/Broadcast para todos os consumidores no grupo
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "chat.message",
                "message": body_message,
                "user": self.user.id # type: ignore
            }
        )

    # Client receives message from room group/Broadcast do grupo
    # chatSocket.onmessage
    async def chat_message(self, event):
        message = event["message"]
        user = event["user"]

        # Send message to WebSocket/Client
        await self.send(text_data=json.dumps({
            "time": datetime.now().strftime("%H:%M"),
            "message": message,
            "user": user
        })
        )

    @database_sync_to_async
    def create_message(self, chat_uuid, author, body_message):
        chat = Chat.objects.get(chat_uuid=chat_uuid)
        return ChatMessage.objects.create(
            chat = chat,
            author = author,
            body = body_message
        )


class OnlineConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"] #type: ignore
        self.room_group_name = "online_users"

        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        connection_type = data.get("type")
        message_user_id = data.get("user_id")

        await self.set_user_status(message_user_id, connection_type)
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "user.status",
                "status": connection_type,
                "user_id": message_user_id
            }
        )

    # AQUI
    # Note that the event you send must have a type key, even if only one
    # type of message is being sent over the channel, as it will turn into
    # an event a consumer has to handle.
    async def user_status(self, event):
        status = True if event["status"] == "open" else False
        user_id = event["user_id"]

        await self.send(text_data=json.dumps({
            "status": status,
            "user_id": user_id,
        }))
    
    @database_sync_to_async
    def set_user_status(self, user_id, status):
        try:
            user = UserOnlineStatus.objects.get(user__id=user_id)
        except UserOnlineStatus.DoesNotExist:
            user = UserOnlineStatus.objects.create(
                user_id = user_id, 
                online_status = False
            )

        user.online_status = True if status == 'open' else False
        user.save()
