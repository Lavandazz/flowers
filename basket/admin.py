from django.contrib import admin

from basket.models import Basket
from shop.models import Category

# Register your models here.


class BasketAdminTab(admin.TabularInline):
    # Для привязки корзины к пользователю в админке
    model = Basket
    fields = ('user', 'product', 'quantity')
    extra = 1


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('user_display', 'product', 'quantity', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('created_at',)

    def user_display(self, obj):
        if obj.user:
            return obj.user.username
        return 'Аноним'


