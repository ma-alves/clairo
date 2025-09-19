from .forms import SignUpForm

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = SignUpForm()
    
    return render(request, 'registration/signup.html', {'form': form})
