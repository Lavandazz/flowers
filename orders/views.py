from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import render, redirect

from basket.models import Basket
from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem


# Create your views here.

@login_required
def create_order(request):
    if request.method == 'POST':
        form = CreateOrderForm(data=request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = request.user
                    basket_items = Basket.objects.filter(user=user)
                    if basket_items.exists():
                        # Создание заказа (адрес, телефон...)
                        order = Order.objects.create(
                            user=user,
                            phone_number=form.cleaned_data['phone_number'],
                            request_delivery=form.cleaned_data['requires_delivery'],
                            delivery_address=form.cleaned_data['delivery_address'],
                            payment_on_get=form.cleaned_data['payment_on_get'],
                        )
                        for basket_item in basket_items:
                            product = basket_item.product
                            name = basket_item.product.name
                            quantity = basket_item.quantity
                            price = basket_item.product.price

                            # Окончательный заказ (продукт, доставка...)
                            OrderItem.objects.create(
                                order=order,
                                product=product,
                                name=name,
                                quantity=quantity,
                                price=price,
                            )
                        # Очищаем корзину пользователя
                        basket_items.delete()
                        messages.success(request, 'Заказ оформлен')
                        return redirect('user:profile')

            except ValidationError as e:
                messages.success(request, str(e))
                return redirect('orders:create_order')

    else:
        # Если пользователь авторизован, то заполняем данные из request
        initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        }
        form = CreateOrderForm(initial=initial)

    context = {'form': form,
               'title': 'Оформление заказа',
               'order': True}
    return render(request, "create_order.html", context=context)
