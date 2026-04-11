from django.db import models

from page.utils import PAGE_TYPES, get_page_display


# Create your models here.


class CompanyInfo(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование', default='Default')
    inn = models.CharField(max_length=12, verbose_name='ИНН')
    ogrn = models.CharField(max_length=13, verbose_name='ОГРН')
    street = models.CharField(max_length=300, verbose_name='Улица')
    house = models.CharField(max_length=20, verbose_name='Дом')
    building = models.CharField(max_length=20, verbose_name='Строение', blank=True, null=True)

    class Meta:
        db_table = 'company_info'
        verbose_name = 'Реквизиты'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Phone(models.Model):
    company = models.ForeignKey(CompanyInfo, on_delete=models.DO_NOTHING, related_name='phones')
    telephone = models.CharField(max_length=10, verbose_name='Номер телефона')

    class Meta:
        db_table = 'phone'
        verbose_name = 'Телефон'
        verbose_name_plural = verbose_name


class Email(models.Model):
    company = models.ForeignKey(CompanyInfo, on_delete=models.DO_NOTHING, related_name='emails')
    email = models.CharField(max_length=70, verbose_name='Электронная почта')

    class Meta:
        db_table = 'email'
        verbose_name = 'Почта'
        verbose_name_plural = verbose_name


class PointPolicy(models.Model):
    """Пункты политики"""
    company = models.ForeignKey(CompanyInfo, on_delete=models.CASCADE, related_name='main_points')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядковый индекс')
    point = models.CharField(max_length=150, verbose_name='Пункт')

    class Meta:
        ordering = ['order']  # сортировка для adminsortable2
        db_table = 'main_point'
        verbose_name = 'пункт политики'
        verbose_name_plural = 'Главные пункты политики'

    def __str__(self):
        return self.point


class Policy(models.Model):
    point = models.ForeignKey(PointPolicy, on_delete=models.CASCADE, related_name='points')
    order = models.PositiveIntegerField(default=0, db_index=True, verbose_name='Индекс отображения пункта')
    description = models.TextField(verbose_name='Текст')

    class Meta:
        ordering = ['order']
        db_table = 'policy'
        verbose_name = 'пункты'
        verbose_name_plural = 'Политика'

    def __str__(self):
        return self.description[:30]


class SEO(models.Model):
    page_type = models.CharField(
        max_length=20,
        choices=PAGE_TYPES,
        unique=True,
        verbose_name='Тип страницы'
    )
    title = models.CharField(max_length=80, verbose_name='Заголовок (title)')
    description = models.CharField(max_length=250, verbose_name='Описание (description)')

    def __str__(self):
        return f"SEO для {get_page_display(str(self.page_type))}"

    class Meta:
        db_table = 'seo'
        verbose_name = 'SEO настройка'
        verbose_name_plural = 'SEO настройки'
