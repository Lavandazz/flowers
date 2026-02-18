from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


app_name = 'user'

# Страница каталога
urlpatterns = [
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('profile/', views.profile, name='profile'),
    path('user-basket/', views.user_basket, name='user_basket'),
    path('logout/', views.logout, name='logout'),

]
