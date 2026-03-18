from django.db import models

from shop.models import Product
from users.models import User


# Create your models here.

class BasketQuerySet(models.QuerySet):
    def total_price(self) -> int:
        """ Сумма цен всех товаров пользователя в корзине """
        return sum(basket.products_price() for basket in self)

    def total_quantity(self) -> int:
        """ Сумма товаров в корзине """
        if self:
            return sum(basket.quantity for basket in self)
        return 0


class Basket(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.IntegerField(default=0, verbose_name='Количество')
    session_key = models.CharField(max_length=32, null=True, blank=True)  # сессия, если пользователь не зареген
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        verbose_name = 'Корзину'
        verbose_name_plural = 'Товары в корзине (не оформлены)'

    objects = BasketQuerySet.as_manager()  # переопределяем

    def products_price(self):
        return round(self.product.price * self.quantity, 2)

    def __str__(self):
        user_info = self.user.username if self.user else f"Аноним (сессия: {self.session_key})"
        return f'Корзина {user_info} | Товар {self.product.name} | Количество {self.quantity}'
