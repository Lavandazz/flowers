from django.contrib import admin

from page.models import Phone, Email, CompanyInfo


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
    list_display = ('id', 'inn', 'ogrn', 'street', 'house', 'company_phone', 'company_email')
    list_display_links = ('id', 'street', 'inn', 'ogrn')
    fields = [('inn', 'ogrn'), ('street', 'house', 'building')]

    def company_phone(self, obj):
        """
        Возврат списка телефонов
        """
        return ', '.join([p.telephone for p in obj.phone.all()])

    def company_email(self, obj):
        """
        Возврат списка телефонов
        """
        return ', '.join([e.email for e in obj.email.all()])
