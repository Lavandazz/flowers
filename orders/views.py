from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView

from basket.models import Basket
from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem


# Create your views here.


class CreateOrderView(LoginRequiredMixin, FormView):
    template_name = "create_order.html"
    form_class = CreateOrderForm
    success_url = reverse_lazy('user:profile')

    def get_initial(self):
        """
        Метод заполняет поля формы
        """
        initial = {
                    'first_name': self.request.user.first_name,
                    'last_name': self.request.user.last_name,
                }
        return initial

    def form_valid(self, form):
        """
        Работа с формой заказа
        """

        try:
            with transaction.atomic():
                user = self.request.user
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
                    messages.success(self.request, 'Заказ оформлен')
                    return redirect('user:profile')

        except ValidationError as e:
            messages.success(self.request, str(e))
            return redirect('orders:create_order')

    def form_invalid(self, form):
        """
        Метод вывозит сообщение об ошибке при заполнении формы
        """
        messages.error(self.request, 'Заполните все поля')
        return redirect('orders:create_order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Оформление заказа'
        context['order'] = True
        return context


# @login_required
# def create_order(request):
#     if request.method == 'POST':
#         form = CreateOrderForm(data=request.POST)
#         if form.is_valid():
#             try:
#                 with transaction.atomic():
#                     user = request.user
#                     basket_items = Basket.objects.filter(user=user)
#                     if basket_items.exists():
#                         # Создание заказа (адрес, телефон...)
#                         order = Order.objects.create(
#                             user=user,
#                             phone_number=form.cleaned_data['phone_number'],
#                             request_delivery=form.cleaned_data['requires_delivery'],
#                             delivery_address=form.cleaned_data['delivery_address'],
#                             payment_on_get=form.cleaned_data['payment_on_get'],
#                         )
#                         for basket_item in basket_items:
#                             product = basket_item.product
#                             name = basket_item.product.name
#                             quantity = basket_item.quantity
#                             price = basket_item.product.price
#
#                             # Окончательный заказ (продукт, доставка...)
#                             OrderItem.objects.create(
#                                 order=order,
#                                 product=product,
#                                 name=name,
#                                 quantity=quantity,
#                                 price=price,
#                             )
#                         # Очищаем корзину пользователя
#                         basket_items.delete()
#                         messages.success(request, 'Заказ оформлен')
#                         return redirect('user:profile')
#
#             except ValidationError as e:
#                 messages.success(request, str(e))
#                 return redirect('orders:create_order')
#
#     else:
#         # Если пользователь авторизован, то заполняем данные из request
#         initial = {
#             'first_name': request.user.first_name,
#             'last_name': request.user.last_name,
#         }
#         form = CreateOrderForm(initial=initial)
#
#     context = {'form': form,
#                'title': 'Оформление заказа',
#                'order': True}
#     return render(request, "create_order.html", context=context)
