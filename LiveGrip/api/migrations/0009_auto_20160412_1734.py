# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-12 17:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_remove_user_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='app_version',
            field=models.CharField(blank=True, default='undefined', max_length=10),
        ),
        migrations.AlterField(
            model_name='user',
            name='gcm_id',
            field=models.CharField(blank=True, default='not_set', max_length=500),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=models.CharField(blank=True, max_length=300),
        ),
    ]