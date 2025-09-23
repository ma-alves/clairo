import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

from chat.models import Chat, ChatMessage


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.chat_uuid = self.scope['url_route']['kwargs']['chat_uuid'] 
        self.chat = get_object_or_404(Chat, group_name=self.chat_uuid)
        
        async_to_sync(self.channel_layer.group_add)(
            self.chat_uuid, self.channel_name
        )
        
        # add and update online users
        # if self.user not in self.chat.online_users.all():
        #     self.chat.online_users.add(self.user)
        #     self.update_online_count()
        
        self.accept()
        
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chat_uuid, self.channel_name
        )
        # remove and update online users
        # if self.user in self.chat.online_users.all():
        #     self.chat.online_users.remove(self.user)
        #     self.update_online_count() 
        
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json['body']
        
        message = ChatMessage.objects.create(
            body = body,
            author = self.user, 
            chat = self.chat
        )
        event = {
            'type': 'message_handler',
            'message_id': message.id,
        }
        async_to_sync(self.channel_layer.group_send)(
            self.chat_uuid, event
        )
        
    def message_handler(self, event):
        message_id = event['message_id']
        message = ChatMessage.objects.get(id=message_id)
        context = {
            'message': message,
            'user': self.user,
            'chat': self.chat
        }
        html = render_to_string("chat/partials/chat_message_p.html", context=context)
        self.send(text_data=html)