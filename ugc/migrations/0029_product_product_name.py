# Generated by Django 3.1.7 on 2021-04-29 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0028_auto_20210429_1312'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_name',
            field=models.CharField(default='', max_length=255, verbose_name='Полное название товара'),
        ),
    ]
