from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from accounts.forms import ResetPasswordForm, SignUpForm, TokenValidationForm, UpdatePasswordForm
from accounts.models import UserToken


def signup_view(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect('token')
		else:
			for field, errors in form.errors.items():
				for error in errors:
					messages.error(request, f'{error}')
	else:
		form = SignUpForm()

	return render(request, 'registration/signup.html', {'form': form})


def token_validation_view(request):
	if request.method == 'POST':
		form = TokenValidationForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			token = form.cleaned_data.get('token')
			try:
				user = User.objects.get(username=username)
				user_token = UserToken.objects.get(user=user)
			except (User.DoesNotExist, UserToken.DoesNotExist):
				messages.error(request, 'Usuário ou token não encontrado.')
			else:
				if str(user_token.token) == str(token):
					login(request, user)
					return redirect('reset-password')
				else:
					messages.error(request, 'Erro ao validar o token.')
	else:
		form = TokenValidationForm()

	return render(request, 'registration/token_validation.html', {'form': form})


@login_required
def update_password_view(request):
	if request.method == 'POST':
		form = UpdatePasswordForm(user=request.user, data=request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)
			messages.success(request, 'Senha alterada com sucesso.')
			return redirect('home')
		else:
			for field, errors in form.errors.items():
				for error in errors:
					messages.error(request, f'{error}')
	else:
		form = UpdatePasswordForm(user=request.user)

	return render(request, 'registration/update_password.html', {'form': form})


@login_required
def reset_password_view(request):
	if request.method == 'POST':
		form = ResetPasswordForm(user=request.user, data=request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)
			messages.success(request, 'Senha alterada com sucesso.')
			return redirect('home')
		else:
			for field, errors in form.errors.items():
				for error in errors:
					messages.error(request, f'{error}')
	else:
		form = UpdatePasswordForm(user=request.user)

	return render(request, 'registration/reset_password.html', {'form': form})


@login_required
def token(request):
	token = request.user.token
	return render(request, 'registration/token.html', {'token': token})
