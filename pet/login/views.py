from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserRegistartionForm, ProfileForm
from django.contrib import auth, messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from orders.models import Order, OrderItem


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
    if request.method == 'POST':
        form = UserRegistartionForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = form.instance
            auth.login(request, user)
            messages.success(
                request, f'{user.username}, Successful Registration'
            )
            return HttpResponseRedirect(reverse('user:login'))
    else:
        form = UserRegistartionForm()
    return render(request, 'login/registration.html')



@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(data=request.POST, isinstance=request.user,
                           files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile was changed')
            return HttpResponseRedirect(reverse('user:profile'))
    else:
        form = ProfileForm(isinstance=request.user)

    orders = Order.objects.filter(user=request.user).prefetch_related(
        Prefetch(
            'items',
            queryset=OrderItem.objects.select_related('product')
        )
    ).order_by('-id') 
    return render(request, 'login/profile.html',
                  {'form': form,
                   'orders': orders})


def logout(request):
    auth.logout(request)
    return redirect(reverse("main:product_list"))