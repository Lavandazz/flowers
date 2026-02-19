from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


app_name = 'basket'

# Страница корзины
urlpatterns = [
    path('basket_add/<slug:product_slug>', views.basket_add, name='basket_add'),
    path('basket_change/<slug:product_slug>', views.basket_change, name='basket_change'),
    path('basket_remove/<int:basket_id>', views.basket_remove, name='basket_remove'),
]
