from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from accounts.forms import SignUpForm, TokenResetPasswordForm


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


def token_reset_view(request):
	if request.method == 'POST':
		form = TokenResetPasswordForm(user=request.user, data=request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Senha alterada com sucesso.')
			return redirect('login')
		else:
			for field, errors in form.errors.items():
				for error in errors:
					messages.error(request, f'{error}')
	else:
		form = TokenResetPasswordForm(user=request.user)

	return render(request, 'registration/reset_password.html', {'form': form})


@login_required
def token(request):
	token = request.user.token
	return render(request, 'registration/token.html', {'token': token})
