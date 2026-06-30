from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.


class Type(models.Model):
    name = models.CharField("Тип категории", max_length=100)
    slug = models.SlugField('URL', unique=True)

    class Meta:
        verbose_name = "Тип категории"
        verbose_name_plural = "I Управление типами товаров"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField("Название", max_length=100)
    slug = models.SlugField('URL', unique=True)
    # models.PROTECT не позволяет удалить тип, пока есть связанные категории
    type = models.ForeignKey(Type, models.PROTECT,
                             related_name='categories',
                             verbose_name='Тип категории')

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "II Управление категориями товаров"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop:catalogue_by_category', args=[self.slug])


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование товара')
    slug = models.SlugField('URL', unique=True)
    categories = models.ManyToManyField(Category,
                                        related_name='products',
                                        verbose_name='Категории')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering: list[str] = ['id']
        db_table = 'products'
        verbose_name = 'Товар'
        verbose_name_plural = 'III Добавление товаров'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """ Перенаправление на страницу товара """
        return reverse('shop:product_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ImageProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='Фото товара')
    image = models.ImageField(upload_to='products/', verbose_name='Изображение')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок отображения')

    class Meta:
        # db_table = 'images'
        ordering = ['order']
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товаров'

    def __str__(self):
        return f'Изображение для {self.product.name}'


class SaleBanner(models.Model):
    title = models.CharField(max_length=100, verbose_name='Наименование акции')
    description = models.CharField(max_length=400, verbose_name='Описание акции')
    image = models.ImageField(verbose_name='Изображение', upload_to='sale/')
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активен', default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']
        db_table = 'banner'
        verbose_name = 'Баннер'
        verbose_name_plural = 'IV Управление баннерами'

    def __str__(self):
        return self.title

