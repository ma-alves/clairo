from django.contrib.auth.models import User
from django.test import TestCase

from accounts.utils import cipher_suite


class UserAuthTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(username='usuario_de_teste', password='Senha1234!')

    def test_token_view(self):
        self.client.force_login(self.user1)
        response = self.client.get('/accounts/token/')

        decrypted_token = cipher_suite.decrypt(
            self.user1.token.token.encode() # type: ignore
        ).decode()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(decrypted_token, response.context['token'])