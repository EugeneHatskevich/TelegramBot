# Generated by Django 3.1.7 on 2021-02-27 16:33

from django.db import migrations, models
import ugc.models


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0026_auto_20210227_1933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activemonitoring',
            name='id_monitoring',
            field=models.PositiveIntegerField(default=ugc.models.f, unique=True, verbose_name='ID мониторинга'),
        ),
    ]
