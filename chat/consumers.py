from datetime import datetime
import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from chat.exceptions import ClientError
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

    async def receive(self, text_data):
        data = json.loads(text_data)
        try:
            if "message" not in data:
                raise ClientError("Mensagem Invalida")
            body_message = data["message"]
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                "error": "Formato JSON Invalido"
            }))
            await self.close()
            return
        except ClientError as e:
            await self.send(text_data=json.dumps({
                "error": e.code
            }))
            await self.close()
            return

        await self.create_message(self.room_name, self.user, body_message)
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "chat.message",
                "message": body_message,
                "user": self.user.id # type: ignore
            }
        )

    async def chat_message(self, event):
        message = event["message"]
        user = event["user"]

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
        self.user = self.scope["user"] # type: ignore
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
        try:
            connection_type, message_user_id = self.check_text_data(data)
        except ClientError as e:
            await self.send(text_data=json.dumps({
                "error": e.code
            }))
            return

        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "user.status",
                "status": connection_type,
                "user_id": message_user_id
            }
        )
        await self.set_user_status(message_user_id, connection_type)

    async def user_status(self, event):
        status = True if event["status"] == "open" else False
        user_id = event["user_id"]
            
        await self.send(text_data=json.dumps({
            "status": status,
            "user_id": user_id,
        }))

    def check_text_data(self, data):
        connection_type = data.get("type")
        message_user_id = data.get("user_id")

        if connection_type not in ["open", "closed"]:
            raise ClientError("Status Invalido")
        
        if not isinstance(message_user_id, int):
            raise ClientError("Id Invalido")
        
        return connection_type, message_user_id

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
