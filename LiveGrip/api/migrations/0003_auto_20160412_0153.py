# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-12 01:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_user_gcm_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gcm_id',
            field=models.CharField(default='not_set', max_length=500),
        ),
    ]