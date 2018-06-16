# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2018-06-15 03:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0039_auto_20180613_2033'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoginHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='VisitHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accessed_at', models.DateTimeField(auto_now_add=True)),
                ('interviewee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interviewee', to=settings.AUTH_USER_MODEL)),
                ('visitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visitors', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='article',
            name='type',
            field=models.IntegerField(default=1, verbose_name='\u6587\u7ae0\u5206\u7c7b'),
        ),
    ]