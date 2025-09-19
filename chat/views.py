from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic.detail import DetailView


def home(request):
    context = {}
    return render(request, "base.html", context)


class UserDetailView(DetailView):
    model = User
    template_name = "chat/profile.html"
