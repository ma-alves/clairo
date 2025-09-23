import shortuuid

from django.db import models
from django.contrib.auth.models import User


class Chat(models.Model):
    chat_uuid = models.CharField(max_length=128, unique=True, default=shortuuid.uuid)
    users = models.ManyToManyField(User, related_name='chats', blank=True)
    online_users = models.ManyToManyField(User, related_name='online_chats', blank=True)
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return self.chat_uuid
    
    def save(self, *args, **kwargs):
        if not self.chat_uuid:
            self.chat_uuid = shortuuid.uuid()
        super().save(*args, **kwargs)


class ChatMessage(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=1000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.body:
            return f'{self.author.username} : {self.body}'
        
    class Meta:
        ordering = ['-created_at']
