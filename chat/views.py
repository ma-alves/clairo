from django.shortcuts import render


def home(request):
    context = {}
    return render(request, "base.html", context)

def login(request):
    return render(request, "chat/login.html")

def profile(request):
    return render(request, "chat/profile.html")