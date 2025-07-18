from django.shortcuts import render
from .forms import UserLoginForm
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.urls import reverse

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username,
                                     password=password)
            
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('main:product'))
            
    else:
        form = UserLoginForm

    return render(request, 'login/login.html', {'form': form})


def register(request):
    return render(request, 'login/register.html')

def profile(request):
    return render(request, 'login/profile.html')


def logout(request):
    pass