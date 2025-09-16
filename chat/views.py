from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView


def home(request):
    context = {}
    return render(request, "base.html", context)


class UserDetailView(DetailView):
    model = User
    template_name = "chat/profile.html"


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


def logout_view(request):
    logout(request)
    return redirect("home")