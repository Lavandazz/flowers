from django.db import models

# Create your models here.


class CompanyInfo(models.Model):
    inn = models.CharField(max_length=12, verbose_name='ИНН')
    ogrn = models.CharField(max_length=13, verbose_name='ОГРН')
    street = models.CharField(max_length=300, verbose_name='Улица')
    house = models.CharField(max_length=20, verbose_name='Дом')
    building = models.CharField(max_length=20, verbose_name='Строение', blank=True, null=True)

    class Meta:
        db_table = 'company_info'
        verbose_name = 'Реквизиты'
        verbose_name_plural = verbose_name


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

