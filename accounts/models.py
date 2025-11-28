import secrets

from django.db import models
from django.contrib.auth.models import User


class UserToken(models.Model):
	user = models.OneToOneField(User, related_name='token', on_delete=models.CASCADE)
	# token = models.CharField(max_length=64, default=secrets.token_hex, unique=True)
	token = models.CharField(max_length=64, default=lambda: secrets.token_hex(16), unique=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self) -> str:
		return f'{self.token}'
