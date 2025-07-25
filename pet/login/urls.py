from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='registration'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
]

