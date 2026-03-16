from django.db import models
from django.urls import reverse
from django.utils.html import format_html

from shop.models import Product
from users.models import User


# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, null=True, default=True, verbose_name='Пользователь')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона')
    request_delivery = models.BooleanField(default=False, verbose_name='Требуется доставка')
    delivery_address = models.TextField(null=True, blank=True, verbose_name='Адрес доставки')
    payment_on_get = models.BooleanField(default=False, verbose_name='Оплата при получении')
    is_paid = models.BooleanField(default=False, verbose_name='Оплачено')
    status = models.CharField(max_length=50, default='В обработке', verbose_name='Статус заказа')

    class Meta:
        db_table = 'orders'
        verbose_name = 'Заказ | Пользователь'
        verbose_name_plural = 'Управление заказами'

    def __str__(self):
        return f'Заказ № {self.pk}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.SET_DEFAULT, verbose_name='Товар', null=True, default=True)
    name = models.CharField(max_length=150, verbose_name='Название')
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата продажи')

    class Meta:
        db_table = 'order_item'
        verbose_name = 'Товар'
        verbose_name_plural = 'Купленные товары'

    def products_price(self):
        return round(self.product.price * self.quantity, 2)

    def __str__(self):
        return f'Товар {self.name} | Заказ № {self.order.pk}'


class PaymentOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ', related_name='payments')
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Сумма заказа')
    payment_id = models.CharField(max_length=150, verbose_name='ID платежа в ЮKassa', unique=True)
    status = models.CharField(max_length=50, verbose_name='Статус платежа',
                              default='pending')  # pending, succeeded, canceled
    payment_method = models.CharField(max_length=50, verbose_name='Способ оплаты', blank=True)  # card, cash и т.д.
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата подтверждения')
    description = models.CharField(max_length=150, verbose_name='Описание')

    class Meta:
        db_table = 'payment'
        verbose_name = 'Оплачено'
        verbose_name_plural = 'Статусы оплат'
