from django.contrib import admin

from basket.admin import BasketAdminTab
from orders.admin import OrdersTab
from users.models import User

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    # fields = [('username', 'first_name', 'last_name'), ('email', 'phone_number'), 'is_staff']
    filter_horizontal = ('groups', 'user_permissions',)
    # Настройка формы редактирования пользователя (поля разбиты на группы)
    fieldsets = (
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'groups'),  # 'user_permissions' для точечного изменения прав
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    # Если нужно добавить поля в форму создания нового пользователя (необязательно)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone_number', 'password1', 'password2'),
        }),
    )
    # привязываем корзину к пользователю в админке
    inlines = [BasketAdminTab, OrdersTab]
