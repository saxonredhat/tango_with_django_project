# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2018-06-12 17:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0030_auto_20180613_0107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.CharField(max_length=499),
        ),
    ]
