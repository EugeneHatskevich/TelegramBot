# Generated by Django 3.1.5 on 2021-01-19 11:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0009_auto_20210116_1035'),
    ]

    operations = [
        migrations.CreateModel(
            name='OperatorMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operator_message', models.TextField(choices=[('1', 'One'), ('2', 'Two'), ('3', 'Three')], default='0', max_length=255)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ugc.product', verbose_name='ID товара')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ugc.profile', verbose_name='ID пользователя')),
            ],
        ),
    ]
