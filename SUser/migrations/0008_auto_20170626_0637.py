# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-26 06:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SUser', '0007_auto_20170626_0637'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='admin',
            field=models.TextField(default='[]'),
        ),
        migrations.AddField(
            model_name='department',
            name='admin',
            field=models.TextField(default='[]'),
        ),
    ]
