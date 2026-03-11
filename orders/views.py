
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import CreateView, FormView
from yookassa import Payment

from basket.models import Basket
from common.payment import pay_yookassa
from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem, PaymentOrder
from users.models import User


# Create your views here.


class CreateOrderView(LoginRequiredMixin, FormView):
    template_name = "create_order.html"
    form_class = CreateOrderForm
    success_url = reverse_lazy('user:profile')

    def get_initial(self):
        """
        Метод заполняет поля формы
        """
        user: User = self.request.user
        initial = {
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'phone_number': user.phone_number,
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
                    # Создание заказа (адрес, телефон...) со статусом "ожидает оплаты"
                    order = Order.objects.create(
                        user=user,
                        phone_number=form.cleaned_data['phone_number'],
                        request_delivery=form.cleaned_data['requires_delivery'],
                        delivery_address=form.cleaned_data['delivery_address'],
                        payment_on_get=form.cleaned_data['payment_on_get'],
                        # status='pending'
                    )

                    # Создаём позиции заказа (продукт, доставка...)
                    for basket_item in basket_items:
                        OrderItem.objects.create(
                            order=order,
                            product=basket_item.product,
                            name=basket_item.product.name,
                            quantity=basket_item.quantity,
                            price=basket_item.product.price,
                        )
                    print('СПОСОБ ОПЛАТЫ form.cleaned_data["payment_on_get"]', type(form.cleaned_data['payment_on_get']),form.cleaned_data['payment_on_get'])

                    # 2. Если выбран способ оплаты "картой" (payment_on_get = False), идём в ЮKassa
                    if not int(form.cleaned_data['payment_on_get']):  # оплата картой онлайн
                        total_price = sum(item.product.price * item.quantity for item in basket_items)

                        print('total_price', total_price)

                        self.request.session['last_order_id'] = order.id
                        print('last_order_id',self.request.session['last_order_id'])
                        try:

                            payment = pay_yookassa(order.id, total_price,
                                               return_url=self.success_url)
                        except Exception as e:
                            print('Ошибка вышла', e)

                        order_name = f'Заказ № {order.id}_{total_price}'

                        PaymentOrder.objects.create(
                            order=order,
                            price=total_price,
                            payment_id=payment.id,
                            status=payment.status,
                            description=order_name

                        )
                        print('ПРОВЕДЕН ПЛАТЕЖ ОНЛАЙН НА СУММУ:', total_price)
                        return redirect(payment.confirmation.confirmation_url)

                    print('ГОТОВО')
                    # Очищаем корзину пользователя
                    basket_items.delete()
                    messages.success(self.request, 'Заказ оформлен')
                    return redirect('user:profile')

        except ValidationError as e:
            messages.error(self.request, str(e))
            return redirect('orders:create_order')

        except Exception as e:

            # Логируем ошибку (например, print(e) или в лог-файл)
            messages.error(self.request, 'Ошибка при создании платежа. Попробуйте позже.')
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


def order_success(request):
    order_id = request.session.get('last_order_id')  # нужно сохранить в сессии при создании заказа
    order = Order.objects.get(id=order_id)
    payment_order = order.payments.last()
    if payment_order:
        payment = Payment.find_one(payment_order.payment_id)
        if payment.status == 'succeeded':
            # обновляем статусы
            payment_order.status = 'succeeded'
            payment_order.confirmed_at = timezone.now()
            payment_order.save()

            order.is_paid = True
            order.status = 'Оплачен'
            order.save()

            Basket.objects.filter(user=order.user).delete()
            messages.success(request, 'Оплата прошла успешно!')
        else:
            messages.warning(request, f'Платёж не завершён. Статус: {payment.status}')
    return render(request, 'order_success.html', {'order': order})

