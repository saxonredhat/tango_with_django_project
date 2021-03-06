# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2018-06-21 02:54
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0044_auto_20180620_0907'),
    ]

    operations = [
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('is_read', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_from_user', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_to_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='news_from_user', to=settings.AUTH_USER_MODEL)),
                ('to_article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='news_to_article', to='blog.Article')),
                ('to_comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='news_to_comment', to='blog.Comment')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='news_to_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
