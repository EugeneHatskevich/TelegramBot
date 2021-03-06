# Generated by Django 3.1.4 on 2021-01-11 06:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0003_auto_20210105_1635'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.PositiveIntegerField(unique=True, verbose_name='Внешний ID товара')),
                ('product_name', models.CharField(max_length=255, verbose_name='Название товара')),
                ('product_url', models.CharField(max_length=255, verbose_name='Полный url товара')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.AlterField(
            model_name='message',
            name='text',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ugc.product', verbose_name='Текст'),
        ),
    ]
