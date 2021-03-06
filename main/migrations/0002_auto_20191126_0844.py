# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-11-26 08:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['dt_created'], 'verbose_name': 'Отзыв', 'verbose_name_plural': 'Отзывы'},
        ),
        migrations.AlterField(
            model_name='doctor',
            name='specialty',
            field=models.ManyToManyField(to='main.Specialty', verbose_name='Специальность врача'),
        ),
        migrations.AlterField(
            model_name='review',
            name='dt_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата и время редактирования отзыва'),
        ),
        migrations.AlterField(
            model_name='review',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь, оставивший отзыв'),
        ),
        migrations.AlterField(
            model_name='review',
            name='user_ip',
            field=models.GenericIPAddressField(protocol='IPv4', verbose_name='ip-адрес пользователя'),
        ),
    ]
