# Generated by Django 5.0.1 on 2024-02-12 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_colors_options_masterdata_confirmation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='masterdata',
            name='status',
            field=models.CharField(choices=[('в процессе', 'в процессе'), ('завершень', 'завершень')], default='в процессе', max_length=50),
        ),
    ]
