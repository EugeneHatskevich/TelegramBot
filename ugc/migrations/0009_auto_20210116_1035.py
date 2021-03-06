# Generated by Django 3.1.5 on 2021-01-16 07:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0008_auto_20210111_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='text',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ugc.product', verbose_name='Внешний ID товара'),
        ),
        migrations.CreateModel(
            name='PassiveMonitoring',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monitoring_percent', models.PositiveIntegerField(verbose_name='Процент мониторинга')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ugc.profile', verbose_name='Профиль')),
                ('text', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ugc.product', verbose_name='Внешний ID товара')),
            ],
            options={
                'verbose_name': 'Пассивный мониторинг',
                'verbose_name_plural': 'Пассивный мониторинг',
            },
        ),
        migrations.CreateModel(
            name='ActiveMonitoring',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ugc.profile', verbose_name='Профиль')),
                ('text', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ugc.product', verbose_name='Внешний ID товара')),
            ],
            options={
                'verbose_name': 'Активный мониторинг',
                'verbose_name_plural': 'Активный мониторинг',
            },
        ),
    ]
