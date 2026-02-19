from django.shortcuts import render, redirect

from basket.models import Basket
from shop.models import Product


# Create your views here.


def basket_add(request, product_slug):
    product = Product.objects.get(slug=product_slug)

    if request.user.is_authenticated:
        # Фильтруем по пользователю и конкретному продукту
        baskets = Basket.objects.filter(user=request.user, product=product)
        # если корзина не пустая
        if baskets.exists():
            basket = baskets.first()
            if basket:
                basket.quantity += 1
                basket.save()
        else:
            # если корзина пустая, сохраняем юзера и продукт
            Basket.objects.create(user=request.user, product=product, quantity=1)
    # Перенаправление на страницу, где бы пользователь
    return redirect(request.META['HTTP_REFERER'])


def basket_change(request, product_slug):
    pass


def basket_remove(request, basket_id):
    # Получаем корзину
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    # Перенаправление на страницу, где бы пользователь
    return redirect(request.META['HTTP_REFERER'])
