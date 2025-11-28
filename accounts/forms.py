from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.models import User

from accounts.models import UserToken


class SignUpForm(UserCreationForm):
	# email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ('username', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	# def clean_email(self):
	#     email = self.cleaned_data.get('email')
	#     if User.objects.filter(email=email).exists():
	#         raise forms.ValidationError("Este email já está em uso.")
	#     return email


class TokenValidationForm(forms.Form):
	username = forms.CharField(max_length=150)
	token = forms.CharField(max_length=64)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['username'].label = 'Usuário'
		self.fields['token'].label = 'Token'


class UpdatePasswordForm(SetPasswordForm):

	class Meta:
		model = User
		fields = ('password1', 'password2')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['new_password1'].label = 'Nova senha'
		self.fields['new_password2'].label = 'Confirmar nova senha'