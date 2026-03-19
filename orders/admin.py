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
    """
    Купленные товары
    """
    list_display = ("order", "display_user", "product", "price", "quantity", 'created')
    search_fields = ('name',)

    def display_user(self, obj):
        """Отображение пользователя"""
        return f'{obj.order.user.first_name} {obj.order.user.last_name}'


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

    def title_order(self, rec):
        return f'Заказ № {rec.id}'

    title_order.short_description = 'Заказ | №'
