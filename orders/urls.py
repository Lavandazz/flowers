from django.urls import path

from . import views

app_name = 'orders'
# Страница каталога
urlpatterns = [
    # path('order_message/', views.redirect_message, name='order_message'),
    path('create_order/', views.CreateOrderView.as_view(), name='create_order'),
    path('payment/yookassa-webhook/', views.yookassa_webhook, name='yookassa_webhook'),
]
