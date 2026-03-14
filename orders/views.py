import json
from django.core.cache import cache

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, FormView
from yookassa import Payment

from basket.models import Basket
from common.payment import pay_yookassa, check_payment
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
                print('basket_items', basket_items)
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
                        print('basket_item', basket_item.id)

                    # 2. Если выбран способ оплаты "картой" (payment_on_get = False), идём в ЮKassa
                    if not int(form.cleaned_data['payment_on_get']):  # оплата картой онлайн
                        total_price = sum(item.product.price * item.quantity for item in basket_items)

                        print('total_price заказа', total_price)

                        self.request.session['last_order_id'] = order.id
                        print('last_order_id', self.request.session['last_order_id'])
                        # Строим абсолютный путь для возврата из оплаты в профиль
                        return_url = self.request.build_absolute_uri(reverse('user:profile'))
                        print('return_url', return_url)
                        try:

                            payment = pay_yookassa(order.id, total_price,
                                                   return_url=return_url)
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
                        # После создания платежа сохраняем ключи к заказу и платежу для проверки статуса
                        self.request.session['last_order_id'] = order.id
                        self.request.session['last_payment_id'] = payment.id

                        print('НАЧИНАЮ ОПЛАТУ ОНЛАЙН НА СУММУ:', total_price)
                        # Информация о платеже,
                        # имеет вид https://yoomoney.ru/checkout/payments/v2/contract?orderId=31449a57-000f-5000-b000-18fe245df32b
                        confirmation_url = payment.confirmation.confirmation_url

                        # basket_items.delete()
                        messages.success(self.request, 'Заказ оформлен')

                        # После перенаправления в профиль, необходимо обновить кэш, для того, чтобы обновились заказы

                        return redirect(confirmation_url)

                    print('ГОТОВО')
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


@csrf_exempt
@require_POST
def yookassa_webhook(request):
    """
    Проверка платежа
    """
    try:
        data = json.loads(request.body)
        print('получил data платежа', data)
    except json.JSONDecodeError:
        return HttpResponse(status=400)

    # Извлекаем данные
    payment_id = data['object']['id']
    status = data['object']['status']
    metadata = data['object'].get('metadata', {})
    order_id = metadata.get('order_id')  # если передавали в metadata
    print('извлек данные', payment_id,
          status, order_id)
    if status == 'succeeded':
        check_payment(payment_id=payment_id)

    return HttpResponse(status=200)

