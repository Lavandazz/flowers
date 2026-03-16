from django.contrib import admin

from orders.models import Order, OrderItem, PaymentOrder


# Register your models here.
class OrdersAdminTab(admin.TabularInline):
    model = OrderItem
    extra = 0


class PaymentOrdersAdminTab(admin.TabularInline):
    model = PaymentOrder
    extra = 0


@admin.register(PaymentOrder)
class PaymentOrderAdmin(admin.ModelAdmin):
    list_display = ("order", "payment_id", 'price', 'payment_status', "created_at", 'confirmed_at')
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
    list_display = ("order", "product", "name", "price", "quantity", 'created')
    search_fields = ('name',)


class OrdersTab(admin.TabularInline):
    """
    Отображает в админке данные.
    А так же используется в админке к пользователю
    """
    model = Order
    fields = ('id', 'user', 'status', )
    extra = 0


@admin.register(Order)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('title_order', 'status', 'user', 'is_paid', 'created', 'request_delivery')
    search_fields = ('user', 'created', 'id')
    list_filter = ('status', 'request_delivery', 'created')
    inlines = (OrdersAdminTab, PaymentOrdersAdminTab)  # привязывает товары к заказу

    def title_order(self, rec):
        return f'Заказ № {rec.id}'

    title_order.short_description = 'Заказ | №'
