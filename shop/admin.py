from django.contrib import admin
from image_uploader_widget.admin import ImageUploaderInline

from shop.models import Category, Product, Type, SaleBanner, ImageProduct


# Register your models here.

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}  # slug заполняется из name


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}  # slug заполняется из name
    list_filter = ('type',)


class ProductImageAdmin(ImageUploaderInline):
    model = ImageProduct


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('categories',)
    list_display = ('name', 'display_category', 'price')
    fields = [('name', 'slug'), 'description', 'price', 'categories']
    search_fields = ('name', 'description',)
    list_filter = ('categories', )
    list_display_links = ('name','display_category')
    inlines = [ProductImageAdmin]

    def display_category(self, obj):
        """Отображение категории товара"""
        # Строку из нескольких категорий, так как связь ManyToManyField
        return ', '.join(cat.name.capitalize() for cat in obj.categories.all())

    display_category.short_description = 'Категория'


@admin.register(SaleBanner)
class SaleBannerAdmin(admin.ModelAdmin):
    search_fields = ('title',)
