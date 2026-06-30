"""
Для работы юкассы локально, необходимо пробросить туннель tuna http 8002
Полученный туннель зарегистрировать в тестовом магазине юкассы.
Настроить вебхук по ссылке https://yookassa.ru/my/merchant/integration/http-notifications
Прописать url для получения вебхуков /orders/payment/yookassa-webhook/, например, https://axog62-80-251-231-77.ru.tuna.am/orders/payment/yookassa-webhook/
 и совершать платежи.
"""

from datetime import datetime
import json
import logging

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import FormView

from basket.models import Basket
from common.payment import pay_yookassa, check_payment
from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem, PaymentOrder


logger = logging.getLogger('order')


class CreateOrderView(FormView):
    """
    Предаставление для оформления заказа без регистрации
    """
    template_name = "create_anonim_order.html"
    form_class = CreateOrderForm
    success_url = reverse_lazy('shop:catalogue')


    def form_valid(self, form):
        """
        Работа с формой заказа.
        Если юзер авторизован, то берем корзины из бд. 
        Иначе, передаем данные юхера через session.session_key и фильтруем корзины пользователя по ключу session_key
        """
        try:
            with transaction.atomic():
                user = self.request.user if self.request.user.is_authenticated else None
                if user:
                    basket_items = Basket.objects.filter(user=user)
                else:
                    if not self.request.session.session_key:
                        self.request.session.create()

                    session_key = self.request.session.session_key
                    basket_items = Basket.objects.filter(session_key=session_key)

                logger.debug('Создается заказ к корзине: %s', basket_items)
                if basket_items.exists():
                    # Создание заказа (адрес, телефон...) со статусом "ожидает оплаты"
                    order = Order.objects.create(
                        user=user,
                        phone_number=form.cleaned_data['phone_number'],
                        customer_name=form.cleaned_data['customer_name'],   
                        customer_email=form.cleaned_data['customer_email'], 
                        request_delivery=form.cleaned_data['requires_delivery'],
                        delivery_address=form.cleaned_data['delivery_address'],
                        comment=form.cleaned_data['comment'],
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

                    # Итоговая сумма корзины
                    total_price = sum(item.product.price * item.quantity for item in basket_items)
                    # # После вычисления суммы платежа, удаляем корзину
                    basket_items.delete()
                    # Строим абсолютный путь для возврата из оплаты в профиль http://localhost:8000/user/profile/
                    return_url = self.request.build_absolute_uri(reverse('shop:catalogue'))
                    try:
                        order_name = f'Оплата заказа № {order.id} {datetime.now().isoformat()} в floristka-msk.ru'
                        payment = pay_yookassa(
                            order_id=order.id,
                            order_name=order_name,
                            total_price=total_price,
                            return_url=return_url
                            )
                        
                    except Exception as e:
                        logger.error('Ошибка при создании платежа: %s', e)
                        messages.error(self.request, 'Не удалось создать платёж. Попробуйте позже.')
                        # Откатываем транзакцию (она уже будет откачена автоматически из-за исключения)
                        return redirect('orders:create_order')

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

                    logger.info('ОПЛАТА НА СУММУ: %s', total_price)
                    # Информация о платеже,
                    # имеет вид https://yoomoney.ru/checkout/payments/v2/contract?orderId=31449a57-000f-5000-b000-18fe245df32b
                    confirmation_url = payment.confirmation.confirmation_url
                    
                    logger.info("сохранение пользователя после оформления заказа")

                    messages.success(self.request, 'Заказ оформлен')

                    # После перенаправления в профиль, необходимо обновить кэш, для того, чтобы обновились заказы
                    return redirect(confirmation_url)

        except ValidationError as e:
            messages.error(self.request, str(e))
            return redirect('orders:create_order')

        except Exception as e:
            logger.error('Ошибка при создании платежа. Попробуйте позже., %s', e)
            messages.error(self.request, 'Ошибка при создании платежа. Попробуйте позже.')
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
    В лк Юкасса необходимо указать полностью путь к вебхуку: домен/orders/payment/yookassa-webhook/
    """
    logger.info('Получение yookassa_webhook')
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponse(status=400)

    # Извлекаем данные
    payment_id = data['object']['id']
    status = data['object']['status']
    # metadata = data['object'].get('metadata', {})
    # order_id = metadata.get('order_id')  # если передавали в metadata

    logger.info('Получение yookassa_webhook payment_id - %s, status - %s', payment_id, status)

    if status == 'succeeded':
        check_payment(payment_id=payment_id)

    return HttpResponse(status=200)


def redirect_message(request):
    return render(request, 'order_message.html')


"""
Ниже CreateOrderView используется для оформления заказов только зарегестрированными пользователями. 
На данный момент реализация не используется и не является актуальной. 
В дальнейшем, если в проект будет возвращены ЛК, необходимо будет подкорректировать.
"""
# class CreateOrderView(LoginRequiredMixin, FormView):
#     """
#     Представление для оформления заказа залогиненного пользователя.
#     """
#     template_name = "create_order.html"
#     form_class = CreateOrderForm
#     success_url = reverse_lazy('user:profile')

#     def get_initial(self):
#         """
#         Метод заполняет поля формы
#         """
#         user: User = self.request.user
#         initial = {
#                     'first_name': user.first_name,
#                     'last_name': user.last_name,
#                     'phone_number': user.phone_number,
#                 }

#         return initial

#     def form_valid(self, form):
#         """
#         Работа с формой заказа
#         """

#         try:
#             with transaction.atomic():
#                 user = self.request.user
#                 basket_items = Basket.objects.filter(user=user)
#                 logger.debug('Создается заказ к корзине: %s', basket_items)
#                 if basket_items.exists():
#                     # Создание заказа (адрес, телефон...) со статусом "ожидает оплаты"
#                     order = Order.objects.create(
#                         user=user,
#                         phone_number=form.cleaned_data['phone_number'],
#                         request_delivery=form.cleaned_data['requires_delivery'],
#                         delivery_address=form.cleaned_data['delivery_address'],
#                         comment=form.cleaned_data['comment'],
#                     )

#                     # Создаём позиции заказа (продукт, доставка...)
#                     for basket_item in basket_items:
#                         OrderItem.objects.create(
#                             order=order,
#                             product=basket_item.product,
#                             name=basket_item.product.name,
#                             quantity=basket_item.quantity,
#                             price=basket_item.product.price,
#                         )

#                     # Итоговая сумма корзины
#                     total_price = sum(item.product.price * item.quantity for item in basket_items)

#                     # Строим абсолютный путь для возврата из оплаты в профиль http://localhost:8000/user/profile/
#                     return_url = self.request.build_absolute_uri(reverse('user:profile'))
#                     try:
#                         payment = pay_yookassa(order.id, total_price,
#                                                return_url=return_url)
#                     except Exception as e:
#                         print('Ошибка вышла', e)

#                     order_name = f'Заказ № {order.id}_{total_price}'

#                     PaymentOrder.objects.create(
#                         order=order,
#                         price=total_price,
#                         payment_id=payment.id,
#                         status=payment.status,
#                         description=order_name

#                     )
#                     # После создания платежа сохраняем ключи к заказу и платежу для проверки статуса
#                     self.request.session['last_order_id'] = order.id
#                     self.request.session['last_payment_id'] = payment.id

#                     logger.info('ОПЛАТА НА СУММУ: %s', total_price)
#                     # Информация о платеже,
#                     # имеет вид https://yoomoney.ru/checkout/payments/v2/contract?orderId=31449a57-000f-5000-b000-18fe245df32b
#                     confirmation_url = payment.confirmation.confirmation_url

#                     messages.success(self.request, 'Заказ оформлен')

#                     # После перенаправления в профиль, необходимо обновить кэш, для того, чтобы обновились заказы
#                     return redirect(confirmation_url)

#         except ValidationError as e:
#             messages.error(self.request, str(e))
#             return redirect('orders:create_order')

#         except Exception as e:
#             logger.error('Ошибка при создании платежа. Попробуйте позже., %s', e)
#             messages.error(self.request, 'Ошибка при создании платежа. Попробуйте позже.')
#             return redirect('orders:create_order')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Оформление заказа'
#         context['order'] = True
#         return context

