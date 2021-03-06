# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2018-06-26 12:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0049_follow_is_read'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='favorite',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='like',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
    ]
