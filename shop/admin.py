from django.contrib import admin


from shop.models import Category, Product, Type, SaleBanner


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


@admin.register(SaleBanner)
class SaleBannerAdmin(admin.ModelAdmin):
    # list_display = ('title', 'description', 'is_active')
    search_fields = ('title',)
    # list_editable = ('order', 'is_active')
