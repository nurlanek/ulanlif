# Generated by Django 4.2.9 on 2024-01-22 15:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Kroy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Наименование')),
                ('kroy_no', models.IntegerField(verbose_name='Крой номер')),
                ('ras_tkani', models.FloatField(verbose_name='Расход ткани')),
                ('ras_dublerin', models.FloatField(verbose_name='Расход дублерин')),
                ('edinitsa', models.IntegerField(blank=True, null=True, verbose_name='Единица')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Примечение')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создание')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активен')),
            ],
            options={
                'verbose_name_plural': 'Крой',
            },
        ),
        migrations.CreateModel(
            name='Masterdata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('в процессе', 'в процессе'), ('звершень', 'звершень')], default='в процессе', max_length=50)),
                ('kroy_no', models.IntegerField(verbose_name='Крой номер')),
                ('edinitsa', models.IntegerField(verbose_name='Единица')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активен')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Примечение')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name_plural': 'Общая таблица',
            },
        ),
        migrations.CreateModel(
            name='Kroy_detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pachka', models.CharField(max_length=200, verbose_name='Пачка')),
                ('razmer', models.CharField(max_length=200, verbose_name='Размер')),
                ('rost', models.CharField(max_length=200, verbose_name='Рост')),
                ('stuk', models.IntegerField(verbose_name='Штук')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('kroy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.kroy', verbose_name='Крой')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name_plural': 'Крой детально',
            },
        ),
    ]