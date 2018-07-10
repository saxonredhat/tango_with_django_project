# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from image_cropping import ImageRatioField
from django.contrib.auth.models import User
from datetime import datetime
from time import timezone
from django.db.models import Q
# Create your models here.
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class UserInfo(models.Model):
    user = models.OneToOneField(User,related_name='user_info')
    nickname = models.CharField(max_length=50,default='', blank=True, null=True)
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

class CustomCategory(models.Model):
    name = models.CharField(max_length=50)
    default = models.IntegerField(default=0)
    user = models.ManyToManyField(User)

    class Meta:
        db_table = 'blog_CustomCategory'
        verbose_name_plural = 'CustomCategory'

    def __unicode__(self):
        return self.name


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


class ArticleManager(models.Manager):
    def get_queryset(self):
        return super(ArticleManager,self).get_queryset().filter(~Q(is_deleted=1))

class Article(models.Model):
    title = models.CharField('文章标题', max_length=200)
    #content = RichTextUploadingField('文章内容', config_name='default_ckeditor')
    type = models.IntegerField('文章分类', default=1)
    content = models.TextField('文章内容')
    abstract = models.CharField('文章摘要', max_length=500, null=True , blank=True)
    author = models.ForeignKey(User)
    category = models.ForeignKey(Category)
    custom_category = models.ForeignKey(CustomCategory)
    views = models.IntegerField(default=0)
    pulished_date = models.DateTimeField('发布时间',default=datetime.now)
    is_top = models.BooleanField('置顶',  default=0)
    is_public = models.BooleanField('公开', default=1 )
    is_forbbiden_comment = models.BooleanField('禁止评论',  default=0)
    is_deleted = models.BooleanField('删除',  default=0) # 0：不删除 1：删除
    tags = models.ManyToManyField(Tag)

    objects = ArticleManager()
    class Meta:
        db_table = 'blog_Article'
        verbose_name_plural = 'articles'

    def __unicode__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField()
    article = models.ForeignKey(Article,null=True)
    user = models.ForeignKey(User)
    comt = models.ForeignKey("self",null=True)
    likes = models.IntegerField(default=0)
    is_read = models.BooleanField(default=False)
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
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Favorite(models.Model):
    user = models.ForeignKey(User, null=True)
    article = models.ForeignKey(Article, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='followers')
    followee = models.ForeignKey(User, related_name='followees')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    send_user = models.ForeignKey(User, related_name='message_send_user')  # 私信的发送者
    receive_user = models.ForeignKey(User, related_name='message_receive_user')  # 私信的接收者
    content = models.TextField()  # 私信的内容
    is_read = models.BooleanField(default=0)  # 0:未读 1:已读
    created_at = models.DateTimeField(auto_now_add=True)  # 私信的创建时间


class News(models.Model):
    from_user = models.ForeignKey(User, related_name='news_from_user')  # 消息的发送者
    to_user = models.ForeignKey(User, related_name='news_to_user')  # 消息的接收者用户
    to_article = models.ForeignKey(Article, related_name='news_to_article')  # 消息操作的对象文章
    to_comment = models.ForeignKey(Comment, related_name='news_to_comment')  # 消息操作的对象评论
    type = models.IntegerField()  # 消息的类型 1:关注 2:收藏 3:赞 4:评论
    created_at = models.DateTimeField(auto_now_add=True)  # 消息的创建时间
