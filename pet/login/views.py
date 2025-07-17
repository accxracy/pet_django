from django.shortcuts import render

def login(request):
    return render(request, 'login/login.html')


def register(request):
    return render(request, 'login/register.html')

def profile(request):
    return render(request, 'login/profile.html')


def logout(request):
    pass