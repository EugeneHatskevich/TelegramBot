# Generated by Django 3.1.5 on 2021-01-21 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0010_operatormessage'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='operatormessage',
            options={'verbose_name': 'Сообщение оператора', 'verbose_name_plural': 'Сообщения оператора'},
        ),
        migrations.RemoveField(
            model_name='operatormessage',
            name='operator_message',
        ),
        migrations.AddField(
            model_name='operatormessage',
            name='operator_price',
            field=models.PositiveIntegerField(default=0, verbose_name='Цена оператора'),
        ),
    ]