# Generated by Django 5.0.1 on 2024-02-14 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_masterdata_confirmation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='masterdata',
            name='kroy_no',
            field=models.CharField(max_length=50, verbose_name='Крой номер'),
        ),
    ]