from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


app_name = 'basket'

# Страница корзины
urlpatterns = [
    path('basket_add', views.basket_add, name='basket_add'),
    path('basket_change', views.basket_change, name='basket_change'),
    path('basket_remove', views.basket_remove, name='basket_remove'),
]
