# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-17 01:09
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_auto_20160416_2352'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 4, 17, 1, 9, 43, 178279, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
