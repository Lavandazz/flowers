from django.contrib import admin

from page.models import Requisites


# Register your models here.


@admin.register(Requisites)
class UserAdmin(admin.ModelAdmin):
    list_display = ('telephone', 'email', 'address', 'inn', 'ogrn')
    fields = [('telephone', 'email'), 'address', ('inn', 'ogrn')]

