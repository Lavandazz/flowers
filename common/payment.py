import os
from pathlib import Path

from django.utils import timezone
from dotenv import load_dotenv

from yookassa import Payment, Configuration

from basket.models import Basket
from orders.models import Order

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
        print('payment', payment)
        return payment
    except Exception as e:
        print('Ошибка платежа', e)

