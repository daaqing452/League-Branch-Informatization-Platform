# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-26 06:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SUser', '0006_remove_department_branch'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='suser',
            name='admin_branch',
        ),
        migrations.RemoveField(
            model_name='suser',
            name='admin_department',
        ),
    ]
