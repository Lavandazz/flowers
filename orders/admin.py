import logging

from django.contrib import admin, messages

from common.payment import refund_payment
from orders.models import Order, OrderItem, PaymentOrder


logger = logging.getLogger('pay')


# Register your models here.
class OrdersAdminTab(admin.TabularInline):
    model = OrderItem
    extra = 0


class PaymentOrdersAdminTab(admin.TabularInline):
    model = PaymentOrder
    extra = 0


@admin.register(PaymentOrder)
class PaymentOrderAdmin(admin.ModelAdmin):
    """
    Статусы оплат
    """
    list_display = ("order", "payment_id", 'price', 'payment_status', "created_at", 'confirmed_at', 'is_refunded')
    search_fields = ('order',)

    def payment_status(self, rec):
        if rec.status == 'succeeded':
            return 'Оплачено'
        elif rec.status == 'pending':
            return 'Не оплачено'
        else:
            return 'Отмена'

    payment_status.short_description = 'Статус платежа'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """
    Купленные товары
    """
    list_display = ("order", "display_user", "product", "price", "quantity", 'created')
    search_fields = ('name',)

    def display_user(self, obj: Order):
        """Отображение пользователя"""
        return f'{obj.order.user.first_name} {obj.order.user.last_name}' if obj.order.user else obj.order.customer_name


class OrdersTab(admin.TabularInline):
    """
    Отображает в админке данные.
    А так же используется в админке к пользователю
    """
    model = Order
    fields = ('user', 'status', )
    extra = 0


@admin.register(Order)
class OrdersAdmin(admin.ModelAdmin):
    """
    Управление заказами
    """
    list_display = ('status', 'title_order', 'user', 'is_paid', 'created', 'request_delivery')
    list_display_links = ('status', 'title_order')
    search_fields = ('user', 'created', 'id')
    list_filter = ('status', 'request_delivery', 'created')
    inlines = (OrdersAdminTab, PaymentOrdersAdminTab)  # привязывает товары к заказу
    actions = ['mark_as_processing', 'mark_as_shipped', 'mark_as_completed', 'cancel_order']

    def title_order(self, rec):
        return f'Заказ № {rec.id}'

    title_order.short_description = 'Заказ | №'

    def cancel_order(self, request, queryset):
        """
        Отмена заказа. Инициация возврата средств и смена статуса заказа
        """
        for order in queryset:
            if order.is_paid:
                # Ищем платёж статусом succeeded-оплачено, связанный с заказом
                payment = order.payments.filter(status='succeeded').first()
                logger.info('Отмена заказа %s', payment)
                if payment:
                    try:
                        refund_payment(payment)
                    except Exception as e:
                        print('Ошибка возврата: %s', e)
                        logger.error("Ошибка возврата по заказу %s, : %s", order.id, e)
                        self.message_user(
                            request,
                            f'Ошибка возврата по заказу №{order.id}: {e}',
                            level=messages.ERROR
                        )
                else:
                    self.message_user(
                        request,
                        f'Заказ №{order.id} оплачен, но нет записи успешного платежа',
                        level=messages.WARNING
                    )
            else:
                order.status = 'cancelled'
                order.save()
                logger.info(f'Заказ №{order.id} отменён без возврата средств')
                self.message_user(request, f'Заказ №{order.id} отменён без возврата средств')

    cancel_order.short_description = "Отменить заказ (с возвратом если оплачен)"

    def mark_as_processing(self, request, queryset):
        queryset.update(status='processing')
        self.message_user(request, "Выбранные заказы отмечены как 'В обработке'")

    mark_as_processing.short_description = "Отметить как 'В обработке'"

    def mark_as_shipped(self, request, queryset):
        queryset.update(status='shipped')
        self.message_user(request, "Выбранные заказы отмечены как 'Передан в доставку'")

    mark_as_shipped.short_description = "Отметить как 'Передан в доставку'"

    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed')
        self.message_user(request, "Выбранные заказы отмечены как 'Выполнен'")

    mark_as_completed.short_description = "Отметить как 'Выполнен'"


