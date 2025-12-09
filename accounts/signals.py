import secrets

from dotenv import load_dotenv

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from accounts.models import UserToken
from accounts.utils import cipher_suite


load_dotenv()


@receiver(post_save, sender=User)
def create_reset_password_token(sender, instance, created, **kwargs):
	if created:
		# gera token como string hex
		token_str = secrets.token_hex(16)
		# criptografa a string (não bytes)
		encrypted_token = cipher_suite.encrypt(token_str.encode())
		# decodifica para string base64 para salvar no CharField
		encrypted_token_str = encrypted_token.decode()

		UserToken.objects.create(user=instance, token=encrypted_token_str)
