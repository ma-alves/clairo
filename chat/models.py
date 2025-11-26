import uuid
import secrets

from django.contrib.auth.models import User
from django.db import models


class Chat(models.Model):
	chat_uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
	users = models.ManyToManyField(User, related_name='chats', blank=True)
	online_users = models.ManyToManyField(User, related_name='online_chats', blank=True)

	def __str__(self):
		return self.chat_uuid

	def save(self, *args, **kwargs):
		if not self.chat_uuid:
			self.chat_uuid = uuid.uuid4()
		super().save(*args, **kwargs)


class ChatMessage(models.Model):
	chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	body = models.CharField(max_length=1000, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		if self.body:
			return f'{self.author.username} : {self.body}'

	class Meta:
		ordering = ['-created_at']


class UserOnlineStatus(models.Model):
	user = models.OneToOneField(User, related_name='status', on_delete=models.CASCADE)
	online_status = models.BooleanField(default=False)

	def __str__(self) -> str:
		return f'{self.user.username}'


class UserToken(models.Model):
	user = models.OneToOneField(User, related_name='token', on_delete=models.CASCADE)
	token = models.CharField(max_length=64, default=secrets.token_hex, unique=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self) -> str:
		return f'{self.token}'
