from django.db import models

# Create your models here.


class Requisites(models.Model):
    address = models.CharField(max_length=300, verbose_name='Адрес')
    email = models.CharField(max_length=70, verbose_name='Электронная почта')
    telephone = models.CharField(max_length=10, verbose_name='Номер телефона')
    inn = models.CharField(max_length=12, verbose_name='ИНН')
    ogrn = models.CharField(max_length=13, verbose_name='ОГРН')

    class Meta:
        db_table = 'requisites'
        verbose_name = 'Реквизиты'
        verbose_name_plural = verbose_name

