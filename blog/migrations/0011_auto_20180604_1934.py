# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2018-06-04 11:34
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20180604_1436'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(verbose_name='\u6587\u7ae0\u6807\u9898'),
        ),
    ]
