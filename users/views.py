from django.shortcuts import render, redirect
from django.contrib import messages
from users.forms import CustomRegistrationForm ,LoginForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.db.models import Prefetch

def sign_up(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active = False  
            user.save()

            messages.success(request, 'A confirmation email has been sent. Please check your inbox.')
            return redirect('login')  

        else:
            messages.error(request, 'Please correct the errors below.')

    else:
        form = CustomRegistrationForm()

    return render(request, 'users/register.html', {"form": form})

def sign_in(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    return render(request, 'users/sign_in.html', {'form': form})


def sign_out(request):
    if request.method == "POST":
        logout(request)
    return redirect('login')


