# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-27 14:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20160727_1426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='app_version',
            field=models.CharField(default='unversioned', max_length=30),
        ),
    ]
