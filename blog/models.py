# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'blog_Category'
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return self.name

    class Meta:
        permissions =(
            ('view_category',   'View category'),
        )


class Author(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'blog_Author'
        verbose_name_plural = 'authors'

    def __unicode__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'blog_Tag'
        verbose_name_plural = 'tags'

    def __unicode__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=50)
    content = RichTextUploadingField('文章标题', config_name='default_ckeditor')
    author = models.ForeignKey(Author)
    category = models.ManyToManyField(Category)
    pulished_date = models.DateField()
    tags = models.ManyToManyField(Tag)

    class Meta:
        db_table = 'blog_Article'
        verbose_name_plural = 'articles'

    def __unicode__(self):
        return self.title


class Comment(models.Model):
    content = models.CharField(max_length=500)
    article = models.ForeignKey(Article)
    author = models.ForeignKey(Author)
    pulished_date = models.DateField(blank=True)

    class Meta:
        db_table = 'blog_Comment'
        verbose_name_plural = 'comments'

    def __unicode__(self):
        return self.content
