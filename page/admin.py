from adminsortable2.admin import SortableAdminMixin, SortableTabularInline
from django.contrib import admin

from page.models import Phone, Email, CompanyInfo, Policy, PointPolicy, SEO


# Register your models here.


class PhoneTab(admin.StackedInline):
    """
    """
    model = Phone
    extra = 0


class EmailTab(admin.StackedInline):
    """
    """
    model = Email
    extra = 0


@admin.register(CompanyInfo)
class ContactsAdmin(admin.ModelAdmin):
    inlines = (PhoneTab, EmailTab)
    list_display = ('id', 'name', 'inn', 'ogrn', 'street', 'house', 'company_phone', 'company_email')
    list_display_links = ('id', 'name', 'street', 'inn', 'ogrn')
    fields = [('name', 'inn', 'ogrn'), ('street', 'house', 'building')]

    def company_phone(self, obj):
        """
        Возврат списка телефонов
        """
        return ', '.join([p.telephone for p in obj.phones.all()])

    def company_email(self, obj):
        """
        Возврат списка телефонов
        """
        return ', '.join([e.email for e in obj.emails.all()])


class PolicyInline(SortableTabularInline):
    """Inline-редактирование подпунктов с возможностью перетаскивания"""
    model = Policy
    extra = 1


@admin.register(PointPolicy)
class PointPolicyAdmin(SortableAdminMixin, admin.ModelAdmin):
    """Пункты политики"""
    ordering = ['order']
    list_display = ('order', 'number_point', 'point',)
    list_display_links = ('number_point', 'point',)
    inlines = [PolicyInline]

    def number_point(self, obj):
        """
        Отображает порядковый номер пункта
        """
        return obj.order

    number_point.short_description = 'Индекс пункта'


@admin.register(Policy)
class PolicyAdmin(SortableAdminMixin, admin.ModelAdmin):
    """
    Политика
    """
    list_display = ('order', 'point_name', 'description')
    list_display_links = ('order', 'point_name', 'description')

    def point_name(self, obj):
        return obj.point

    point_name.short_description = 'Пункт'


@admin.register(SEO)
class SEOAdmin(admin.ModelAdmin):
    """
    SEO настройки
    """
    list_display = ('id', 'page_type', 'title', 'description', )
    list_display_links = ('id', 'page_type', )
    list_editable = ('title', 'description', )
