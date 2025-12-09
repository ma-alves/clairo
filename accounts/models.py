from django.db import models
from django.contrib.auth.models import User


class UserToken(models.Model):
	user = models.OneToOneField(User, related_name='token', on_delete=models.CASCADE)
	token = models.CharField(unique=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self) -> str:
		return f'{self.token}'
