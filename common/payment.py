import logging
from django.http import HttpResponse
from django.utils import timezone
from yookassa import Payment, Configuration, Refund
from conf.settings_env import u_settings
from orders.models import Order, PaymentOrder


# Конфигурация подключения юкассы
Configuration.configure(account_id=u_settings.YOOKASSA_SHOP_ID, secret_key=u_settings.YOOKASSA_SECRET_KEY)

logger = logging.getLogger('pay')


def pay_yookassa(order: Order, order_name: str, total_price: int, return_url):
    """
    Создание платежа
    :param order: объект модели Order
    :param order_name: Наименование заказа для чека
    :param total_price: Общая сумма платежа
    :param return_url: Страница для возврата после оплаты
    :return: payment -в озвращается объект платежа с номером и статусом pending
    """
    # Собираем данные для чека
    # Формируем список товаров из OrderItem
    logger.info('ОПЛАТА НАЧИНАЕТСЯ для %s', order_name)
    logger.info('order %s', order)
    receipt_items = []
    for item in order.orderitem_set.all():  # Если related_name = 'orderitem_set' - получаем все товары
        receipt_items.append({
            "description": item.name[:128],
            "quantity": str(item.quantity),
            "amount": {
                "value": f"{item.price:.2f}",
                "currency": "RUB"
            },
            "vat_code": 1,          # Пример: ставка 20%
            "payment_mode": "full_prepayment",
            "payment_subject": "commodity"
        })
    receipt_data = {
        "customer": {
            "email": order.customer_email  # Email покупателя для отправки чека
        },
        "items": receipt_items,
        "tax_system_code": 1  # Ваша система налогообложения (1 — ОСН, 2 — УСН доходы и т.д.)
    }

    try:
        logger.info('Перехожу к созданию оплаты')
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
                    'order_id': order.id  # Чтобы в вебхуке понять, какой заказ оплачен
                },
                'receipt': receipt_data  # Передаём чек
            },
        )
        logger.info('Оплата заказа %s прошла успешно', order_name)
        
        return payment
    
    except Exception as e:
        logger.error('Ошибка при оплате заказа!!!! %s: %s', order_name, e)


def check_payment(payment_id):
    """
    Проверка статуса платежа
    :param payment_id:  payment.id
    """
    # Ниже код проверки без туннелирования сайта, для проверки статуса платежа
    # payment = Payment.find_one(payment_id)
    # if payment.status == 'succeeded' and payment.paid:

    # Сохраняем статус платежа после подтверждения оплаты
    logger.info('check_payment start for %s', payment_id)
    try:
        payment_obj = PaymentOrder.objects.get(payment_id=payment_id)
    except PaymentOrder.DoesNotExist:
        return HttpResponse(status=404)

    payment_obj.status = 'succeeded'
    # Сохраняем статус заказа после подтверждения оплаты
    payment_obj.order.status = 'paid'
    payment_obj.order.is_paid = True
    payment_obj.confirmed_at = timezone.now()
    # Сохранение статуса заказа и платежа
    payment_obj.order.save()
    payment_obj.save()
    logger.info('Успешная оплата %s: ', payment_id)


def refund_payment(payment_obj, total_sum=None):
    """
    Создаёт возврат по платежу.
    payment_obj - экземпляр PaymentOrder
    total_sum - сумма возврата. Если None, возвращается полная сумма.
    """
    payment = Payment.find_one(payment_obj.payment_id)
    # Если статус оплаты не succeeded, то есть не 'Оплачен'
    if payment.status != 'succeeded':
        raise ValueError(f'Платёж {payment_obj.payment_id} не в статусе succeeded: {payment.status}')

    refund_amount = total_sum if total_sum is not None else payment_obj.price

    logger.debug('Сумма возврата refund_amount %s', refund_amount)
    refund = Refund.create({
        "amount": {
            "value": refund_amount,
            "currency": "RUB"
        },
        "payment_id": payment_obj.payment_id,
        'description': f'Возврат по заказу №{payment_obj.order.id}'
    })
    # Обновляем статус платежа и заказа
    payment_obj.status = refund.status  # обычно 'succeeded' или 'pending'
    payment_obj.is_refunded = True  # сохраняем значение возврата
    payment_obj.refunded_at = refund.created_at
    payment_obj.refunded_id = refund.id

    payment_obj.save()

    order = payment_obj.order
    order.status = 'refunded'
    order.save()

    logger.info('Возврат %s: по платежу %s: успешно создан',{refund_amount}, {payment_obj.payment_id})
    return refund




