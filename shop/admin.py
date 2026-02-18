from django.contrib import admin


from shop.models import Category, Product, Type


# Register your models here.

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('name',)}  # slug заполняется из name


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}  # slug заполняется из name


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('categories',)
    list_display = ('name', 'price')

