import os
from pathlib import Path

from django.http import HttpResponse
from django.utils import timezone
from dotenv import load_dotenv

from yookassa import Payment, Configuration

from basket.models import Basket
from orders.models import Order, PaymentOrder

PROJECT_ROOT = Path(__file__).resolve().parent.parent
env_path = PROJECT_ROOT / '.env_pay'

load_dotenv(dotenv_path=env_path)

Configuration.configure(account_id=os.getenv('account_id'), secret_key=os.getenv('secret_key'))


def pay_yookassa(order_id, total_price: int, return_url):
    order_name = f'Заказ № {order_id}_{total_price}'

    print('Принимаю заказ ', order_name)
    try:
        payment = Payment.create(
            {
                'amount': {
                    'value': total_price,
                    'currency': 'RUB'
                },
                'confirmation': {
                    'type': 'redirect',
                    "return_url": return_url
                },
                'capture': True,  # Сразу списать деньги
                'description': order_name,
                'metadata': {
                    'order_id': order_id  # Чтобы в вебхуке понять, какой заказ оплачен
                },
            },
        )
        # payment возвращается объект платежа с номером и статусом pending
        return payment
    except Exception as e:
        print('Ошибка платежа', e)


def check_payment(payment_id):
    """
    Проверка статуса платежа
    :param payment_id:  payment.id
    """
    # payment = Payment.find_one(payment_id)
    # if payment.status == 'succeeded' and payment.paid:

    # Сохраняем статус платежа после подтверждения оплаты
    try:
        payment_obj = PaymentOrder.objects.get(payment_id=payment_id)
    except PaymentOrder.DoesNotExist:
        return HttpResponse(status=404)

    order = payment_obj.order
    print('получил объект платежа', payment_obj)
    print('получил объект order', order)
    payment_obj.status = 'succeeded'
    # Сохраняем статус заказа после подтверждения оплаты
    payment_obj.order.status = 'Оплачен'
    payment_obj.order.is_paid = True

    payment_obj.order.save()

    # Удаляем корзину пользователя после сохранения статусов оплаты
    payment_obj.order.user.basket.all().delete()
    print('КОРЗИНЫ УДАЛЕНЫ', order)

    payment_obj.save()

