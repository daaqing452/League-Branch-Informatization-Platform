# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-27 04:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SUser', '0004_auto_20170527_0336'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='branch',
            name='suser',
        ),
        migrations.AlterField(
            model_name='department',
            name='name',
            field=models.CharField(default='', max_length=64),
        ),
    ]
