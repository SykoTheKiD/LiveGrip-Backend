# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-27 04:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20160726_0144'),
    ]

    operations = [
        migrations.CreateModel(
            name='FirebaseMessagingTokens',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fcm_key', models.CharField(max_length=250, verbose_name='Cloud Token')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name_plural': 'Firebase Tokens',
                'verbose_name': 'Firebase Token',
                'db_table': 'cloud_tokens',
            },
        ),
        migrations.AlterField(
            model_name='accesstoken',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]