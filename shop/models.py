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
    image = models.ImageField(upload_to='products/')

    class Meta:
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


class SaleBanner(models.Model):
    title = models.CharField(max_length=100, verbose_name='Наименование акции')
    description = models.CharField(max_length=400, verbose_name='Наименование акции')
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
