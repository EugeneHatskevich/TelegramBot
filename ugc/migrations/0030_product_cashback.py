# Generated by Django 3.1.7 on 2021-04-29 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0029_product_product_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='cashback',
            field=models.IntegerField(default=0, verbose_name='Кэшбек от Онлайнера'),
        ),
    ]