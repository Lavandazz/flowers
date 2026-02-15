from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.


class Category(models.Model):
    name = models.CharField("Название", max_length=100)
    slug = models.SlugField('URL', unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop:catalogue_by_category', args=[self.slug])


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField('URL', unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='products',
                                 verbose_name='Категория')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

