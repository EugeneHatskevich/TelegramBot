# Generated by Django 3.1.7 on 2021-02-27 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0020_activemonitoring_id_monitoring'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activemonitoring',
            name='id_monitoring',
            field=models.CharField(default=26087203, max_length=255, verbose_name='ID мониторинга'),
        ),
    ]
