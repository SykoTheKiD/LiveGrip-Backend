# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-12 17:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20160412_1734'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='app_version',
            field=models.CharField(default='undefined', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='gcm_id',
            field=models.CharField(default='not_set', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=models.CharField(max_length=300, null=True),
        ),
    ]