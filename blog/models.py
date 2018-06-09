# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
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
    name = models.CharField('名字',max_length=20)

    class Meta:
        db_table = 'blog_Tag'
        verbose_name_plural = 'tags'

    def __unicode__(self):
        return self.name


class Article(models.Model):
    title = models.CharField('文章标题', max_length=50)
    #content = RichTextUploadingField('文章内容', config_name='default_ckeditor')
    type = models.IntegerField('文章类型', default=1)
    content = models.TextField('文章内容')
    abstract = models.CharField('文章摘要', max_length=500, null=True , blank=True)
    author = models.ForeignKey(User)
    category = models.ForeignKey(Category)
    pulished_date = models.DateField('发布时间')
    is_top = models.BooleanField('置顶',  default=0)
    is_public = models.BooleanField('公开', default=1 )
    is_forbbiden_comment = models.BooleanField('禁止评论',  default=0)
    tags = models.ManyToManyField(Tag)

    class Meta:
        db_table = 'blog_Article'
        verbose_name_plural = 'articles'

    def __unicode__(self):
        return self.title


class Comment(models.Model):
    content = models.CharField(max_length=500)
    article = models.ForeignKey(Article,null=True)
    user = models.ForeignKey(User)
    comt = models.ForeignKey("self",null=True)
    pulished_date = models.DateField(blank=True)

    class Meta:
        db_table = 'blog_Comment'
        verbose_name_plural = 'comments'

    def __unicode__(self):
        return self.content
