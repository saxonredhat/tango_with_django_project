# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2018-06-29 14:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0053_auto_20180629_1406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='nickname',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
    ]
