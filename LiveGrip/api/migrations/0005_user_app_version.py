# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-12 04:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='app_version',
            field=models.CharField(default='undefined', max_length=10),
        ),
    ]