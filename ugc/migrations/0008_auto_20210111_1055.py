# Generated by Django 3.1.4 on 2021-01-11 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0007_auto_20210111_1053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='external_id',
            field=models.CharField(max_length=255, unique=True, verbose_name='Внешний ID товара'),
        ),
    ]