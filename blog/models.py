# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from image_cropping import ImageRatioField
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class UserInfo(models.Model):
    user = models.OneToOneField(User,related_name='user_info')
    website = models.URLField(blank=True,null=True)
    picture = models.ImageField(upload_to='profile_images', blank=True, null=True)

    def __unicode__(self):
        return self.user.username


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
    name = models.CharField('名字',max_length=20,unique=True)

    class Meta:
        db_table = 'blog_Tag'
        verbose_name_plural = 'tags'

    def __unicode__(self):
        return self.name


class Article(models.Model):
    title = models.CharField('文章标题', max_length=50)
    #content = RichTextUploadingField('文章内容', config_name='default_ckeditor')
    type = models.IntegerField('文章分类', default=1)
    content = models.TextField('文章内容')
    abstract = models.CharField('文章摘要', max_length=500, null=True , blank=True)
    author = models.ForeignKey(User)
    category = models.ForeignKey(Category)
    views = models.IntegerField(default=0)
    pulished_date = models.DateTimeField('发布时间',default=datetime.now)
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
    likes = models.IntegerField(default=0)
    published_date = models.DateTimeField(default=datetime.now)

    class Meta:
        db_table = 'blog_Comment'
        verbose_name_plural = 'comments'

    def __unicode__(self):
        return self.content

    def get_comments_all(self, include_self=False):
        r = []
        if include_self:
            r.append(self)
        for c in Comment.objects.filter(comt=self):
            _r = c.get_comments_all(include_self=True)
            if 0 < len(_r):
                r.extend(_r)
        return sorted(r ,key=lambda x: x.published_date, reverse=True)


class VisitHistory(models.Model):
    interviewee = models.ForeignKey(User, related_name='interviewee')
    visitor = models.ForeignKey(User, related_name='visitors')
    accessed_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-accessed_at']

class LoginHistory(models.Model):
    pass


class Like(models.Model):
    user_id = models.IntegerField()
    like_article = models.ForeignKey(Article, null=True)
    like_comment = models.ForeignKey(Comment, null=True)
    like_user = models.ForeignKey(User, null=True, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)


class Favorite(models.Model):
    user = models.ForeignKey(User, null=True)
    article = models.ForeignKey(Article, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='followers')
    followee = models.ForeignKey(User, related_name='followees')
    created_at = models.DateTimeField(auto_now_add=True)