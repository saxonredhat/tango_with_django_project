# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2018-06-21 07:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0046_auto_20180621_1252'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Messages',
            new_name='Message',
        ),
    ]
