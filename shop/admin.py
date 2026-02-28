from django.contrib import admin


from shop.models import Category, Product, Type


# Register your models here.

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('name',)}  # slug заполняется из name


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}  # slug заполняется из name
    list_filter = ('type',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('categories',)
    list_display = ('name', 'price')
    search_fields = ('name', 'description',)
    list_filter = ('categories',)

