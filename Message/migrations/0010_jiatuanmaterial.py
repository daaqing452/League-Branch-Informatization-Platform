# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-04 07:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Message', '0009_auto_20170803_0227'),
    ]

    operations = [
        migrations.CreateModel(
            name='JiatuanMaterial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_type', models.CharField(default='.', max_length=1)),
                ('display_id', models.IntegerField(default=0)),
                ('year', models.IntegerField(default=0)),
                ('attachment', models.TextField(default='[]')),
            ],
        ),
    ]
