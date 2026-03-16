from django.contrib import admin

from basket.models import Basket
from shop.models import Category

# Register your models here.


class BasketAdminTab(admin.TabularInline):
    # Для привязки корзины к пользователю в админке
    model = Basket
    fields = ('explanation', 'user', 'product', 'quantity')
    readonly_fields = ('explanation',)
    extra = 0

    def explanation(self, obj):
        # obj — это конкретный объект Basket, но пояснение одинаково для всех строк
        return "Эти товары ещё не заказаны"

    explanation.short_description = 'Примечание'


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('user_display', 'product', 'quantity', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('created_at',)

    def user_display(self, obj):
        if obj.user:
            return obj.user.username
        return 'Аноним'

    user_display.short_description = 'Пользователь'



