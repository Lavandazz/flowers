from django.contrib import admin

from basket.admin import BasketAdminTab
from orders.admin import OrdersTab
from users.models import User

# Register your models here.

# admin.site.register(User)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')

    # привязываем корзину к пользователю в админке
    inlines = [BasketAdminTab, OrdersTab]
