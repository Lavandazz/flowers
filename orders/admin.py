from django.contrib import admin

from orders.models import Order, OrderItem


# Register your models here.
class OrdersAdminTab(admin.TabularInline):
    model = OrderItem
    # fields = ("product", "name", "price", "quantity")
    extra = 0


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
    list_display = ('id', 'status', 'user', 'is_paid', 'created', 'request_delivery')
    search_fields = ('user', 'created', 'id')
    list_filter = ('status', 'request_delivery', 'created')
    inlines = (OrdersAdminTab,)  # привязывает товары к заказу
