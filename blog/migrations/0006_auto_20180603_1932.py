# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2018-06-03 11:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20180603_1930'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ArticleCategory',
            new_name='Category',
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelTable(
            name='category',
            table='blog_Category',
        ),
    ]
