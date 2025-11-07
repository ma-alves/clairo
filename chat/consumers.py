from datetime import datetime
import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from chat.models import Chat, ChatMessage

# Channels are mailboxes that represent users in a group, such as a chat room.
# When a user posts a message, a JavaScript function will transmit the message
# over WebSocket to a ChatConsumer. The ChatConsumer will receive that message
# and forward it to the group corresponding to the room name. Every ChatConsumer
# in the same group (and thus in the same room) will then receive the message
# from the group and forward it over WebSocket back to JavaScript, where it will
# be appended to the chat log.

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
        # Scope contém informações sobre a conexão, incluindo o usuário autenticado e os parâmetros da URL
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

    # Receive message from WebSocket/Client
    # essa porra recebe a mensagem do cliente, processa o caralho que for e aí sim entrega pro grupo
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body_message = text_data_json["message"]
        print(f"Received message: {body_message}") # Apagar depois de testar

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


class OnlineConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"] #type: ignore
        self.room_group_name = "online_users"

        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        await self.set_user_online(True)
        await self.accept()


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )
        await self.set_user_online(False)


    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get("type")

        # talvez fazer a coisa de checar online aqui
        if message_type == "check_user_status":
            user_id = text_data_json.get("user_id")
            if user_id:
                is_online = await self.check_user_online_status(user_id)
                await self.send(text_data=json.dumps({
                    "type": "user_status_response",
                    "user_id": user_id,
                    "is_online": is_online
                }))


    async def user_status(self, event):
        user = event["user"]
        status = event["status"]

        await self.send(text_data=json.dumps({
            "user": user,
            "status": status
        }))
    
    
    @database_sync_to_async
    def set_user_online(self, is_online):
        if is_online:
            user_chats = Chat.objects.filter(users=self.user)
            for chat in user_chats:
                chat.online_users.add(self.user)
        else:
            user_chats = Chat.objects.filter(users=self.user)
            for chat in user_chats:
                chat.online_users.remove(self.user)


    @database_sync_to_async
    def check_user_online_status(self, user_id):
        user_chats = Chat.objects.filter(users__id=user_id)
        for chat in user_chats:
            if chat.online_users.filter(id=user_id).exists():
                return True
        return False