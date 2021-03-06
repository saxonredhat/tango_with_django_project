# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2018-06-03 11:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20180603_1929'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'verbose_name_plural': 'articles'},
        ),
        migrations.AlterModelOptions(
            name='articlecategory',
            options={'verbose_name_plural': 'ArticleCategories'},
        ),
        migrations.AlterModelOptions(
            name='author',
            options={'verbose_name_plural': 'authors'},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name_plural': 'comments'},
        ),
        migrations.AlterModelTable(
            name='article',
            table='blog_Article',
        ),
        migrations.AlterModelTable(
            name='articlecategory',
            table='blog_ArticleCategory',
        ),
        migrations.AlterModelTable(
            name='author',
            table='blog_Author',
        ),
        migrations.AlterModelTable(
            name='comment',
            table='blog_Comment',
        ),
    ]
