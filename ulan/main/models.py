from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

def get_default_user():
    return get_user_model().objects.first()

class Kroy(models.Model):
    class Meta:
            verbose_name_plural = ('Крой')
    name = models.CharField(max_length=250, verbose_name='Наименование')
    kroy_no = models.CharField(max_length=20,verbose_name='Крой номер')
    ras_tkani = models.FloatField(verbose_name='Расход ткани')
    ras_dublerin = models.FloatField(verbose_name='Расход дублерин')
    edinitsa = models.IntegerField(null=True, blank=True, verbose_name='Единица')
    description = models.TextField(null=True, blank=True, verbose_name='Примечение')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создание')
    is_active = models.BooleanField(default=True, verbose_name='Активен')



    def __str__(self):
        return str(self.kroy_no)

class City(models.Model):
    class Meta:
        verbose_name_plural = ('Города')
    name = models.CharField(max_length=100, verbose_name='Город')

    def __str__(self):
        return str(self.name)


class Colors(models.Model):
    class Meta:
        verbose_name_plural = ('Цвет кроя')
    name = models.CharField(max_length=100, verbose_name='Цвет')

    def __str__(self):
       return str(self.name)


class Kroy_detail(models.Model):

    class Meta:
            verbose_name_plural = ('Крой детально')
    kroy = models.ForeignKey(Kroy, on_delete=models.CASCADE, verbose_name='Крой')
    pachka = models.CharField(max_length=200, verbose_name='Пачка')
    razmer = models.CharField(max_length=200, verbose_name='Размер')
    rost = models.CharField(max_length=200, verbose_name='Рост')
    stuk = models.IntegerField(verbose_name='Штук')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    color = models.ForeignKey(Colors, on_delete=models.CASCADE, verbose_name='Цвет')
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='Город')


    def __str__(self):
        return self.pachka

class Masterdata(models.Model):
    class Meta:
            verbose_name_plural = ('Общая таблица')
    OPTION_CHOICES = [
        ('в процессе', 'в процессе'),
        ('завершень', 'завершень'),
    ]
    status = models.CharField(max_length=50, choices=OPTION_CHOICES, default='в процессе')
    kroy_no = models.CharField(max_length=50, verbose_name='Крой номер')
    edinitsa = models.IntegerField(verbose_name='Единица')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    description = models.TextField(null=True, blank=True, verbose_name='Примечение')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    confirmation = models.BooleanField(default=False, verbose_name='Подтверждение')
    operations = models.CharField(max_length=150, verbose_name='Операция')
    type_product = models.CharField(max_length=150, verbose_name='Тип одежды')
    def __str__(self):
        return f"{self.status} - {self.kroy_no}"

class Product_type(models.Model):
    class Meta:
            verbose_name_plural = ('Тип одежды')

    name = models.CharField(max_length=50, verbose_name='Название')


class Operations(models.Model):
    class Meta:
            verbose_name_plural = ('Операции')

    name = models.CharField(max_length=50, verbose_name='Наименование')
    price = models.IntegerField(verbose_name='Цена')
    kroy = models.ForeignKey(Kroy, on_delete=models.CASCADE, verbose_name='Крой')

