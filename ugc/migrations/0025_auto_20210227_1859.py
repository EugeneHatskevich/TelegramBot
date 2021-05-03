# Generated by Django 3.1.7 on 2021-02-27 15:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0024_auto_20210227_1807'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='operatormessagewaiting',
            name='product',
        ),
        migrations.RemoveField(
            model_name='operatormessagewaiting',
            name='profile',
        ),
        migrations.AddField(
            model_name='operatormessagewaiting',
            name='monitoring',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='ugc.activemonitoring', verbose_name='ID мониторинга'),
            preserve_default=False,
        ),
    ]