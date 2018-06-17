# -*- coding:utf-8 -*-
from django import template
from django.contrib.auth.models import User,Group,Permission
from django.template.base import TemplateSyntaxError,NodeList
from blog.models import *
from markdown import markdown
from django.shortcuts import render
#from guardian.core import ObjectPermissionChecker
import re
#import datetime
register = template.Library()
import sys
sys.setrecursionlimit(5000)

@register.filter
def del_html_tag(content):
    return re.sub(r'<[^>]*>', '', content)


@register.filter
def my_markdown(content):
    return markdown(content)


@register.filter
def cut_name(content):
    return content[0:5]


@register.filter
def cut_name_dot(content):
    if len(content) > 5:
        return '...'
    return ''


@register.filter
def get_item(dictionary, key):
    return dictionary[key]


@register.filter
def get_name_tail(content):
    return content[5:]


@register.simple_tag
def replies_of_comment(comment_id):
    counts = 0
    comment = Comment.objects.get(id=comment_id)
    if comment.comment_set.all().count():
        for c in comment.comment_set.all():
            counts += 1
            counts += replies_of_comment(c.id)
    else:
        return 0
    return counts


@register.simple_tag
def user_article_count(user, article_type):
    counts = Article.objects.filter(author=user, type=article_type).count()
    return counts


@register.simple_tag
def user_get_comment_count(user):
    counts=0
    for article in  Article.objects.filter(author=user):
        counts+=article.comment_set.all().count()
    return counts


@register.simple_tag
def user_get_like_count(user):
    counts = 0
    #评论获得的赞数
    for comment in Comment.objects.filter(user=user):
        counts += comment.like_set.all().count()
    #文章获得的赞数
    for article in Article.objects.filter(author=user):
        counts += article.like_set.all().count()
    #用户获得的赞数
    #暂时没有开发该功能
    return counts


#获取关注的boolean结果
@register.assignment_tag
def is_follow(followee,follower):
    try:
        follow=Follow.objects.get(followee=followee,follower=follower)
        if follow:
            return True
        return False
    except Exception, e:
        print Exception, e
        return False


#判断用户是否对文章点赞，返回boolean结果
@register.assignment_tag
def is_like_article(article,user):
    try:
        like = Like.objects.filter(like_article=article, user_id=user.id)
        if like:
            return True
    except Exception, e:
        print Exception, e
        return False


#判断用户是否对评论点赞，返回boolean结果
@register.assignment_tag
def is_like_comment(comment, user):
    try:
        like = Like.objects.filter(like_comment=comment, user_id=user.id)
        if like:
            return True
    except Exception, e:
        print Exception, e
        return False


@register.assignment_tag
def is_favorite_article(article, user):
    try:
        favorite=Favorite.objects.filter(article=article,user=user)
        if favorite:
            return True
    except Exception, e:
        print Exception, e
        return False


#判断文章的类型
@register.simple_tag
def article_type(article_id):
    try:
        article = Article.objects.get(id=article_id)
        if article.type == 1:
            return '原创'
        elif article.type == 2:
            return '翻译'
        elif article.type == 3:
            return '转载'
        else:
            return '其他'

    except Exception,e:
        print Exception,e
        return {'text-color': '', 'type': ''}


#判断文章的类型
@register.simple_tag
def article_color(article_id):
    try:
        article = Article.objects.get(id=article_id)
        if article.type == 1:
            return 'success'
        elif article.type == 2:
            return 'warning'
        elif article.type == 3:
            return 'danger'
        else:
            return 'info'

    except Exception,e:
        print Exception,e
        return {'text-color': '', 'type': ''}


@register.tag("ifuserperm")
def do_ifuserperm(parser, token):
    bits = list(token.split_contents())
    if len(bits) != 3:
        raise TemplateSyntaxError("%r takes two arguments" % bits[0])
    end_tag = 'end' + bits[0]
    nodelist_true = parser.parse(('else', end_tag))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse((end_tag,))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()
    user_obj = parser.compile_filter(bits[1])
    perm_id = parser.compile_filter(bits[2])
    return IfUserPermNode(user_obj, perm_id, nodelist_true, nodelist_false)


class IfUserPermNode(template.Node):
    child_nodelists = ('nodelist_true', 'nodelist_false')

    def __init__(self, user_obj, perm_id, nodelist_true, nodelist_false):
        self.user_obj, self.perm_id = user_obj, perm_id
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false

    def __repr__(self):
        return "<IfUserPermNode>"

    def render(self, context):
        user_obj = self.user_obj.resolve(context, True)
        perm_id = self.perm_id.resolve(context, True)
        perm = Permission.objects.get(id=perm_id)
        perm_str = perm.content_type.app_label + '.' + perm.codename
        if user_obj.has_perm(perm_str):
            return self.nodelist_true.render(context)
        return self.nodelist_false.render(context)


@register.tag("ifgroupperm")
def do_ifgroupperm(parser, token):
    bits = list(token.split_contents())
    if len(bits) != 3:
        raise TemplateSyntaxError("%r takes two arguments" % bits[0])
    end_tag = 'end' + bits[0]
    nodelist_true = parser.parse(('else', end_tag))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse((end_tag,))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()
    group_obj = parser.compile_filter(bits[1])
    perm_id = parser.compile_filter(bits[2])
    return IfGroupPermNode(group_obj, perm_id, nodelist_true, nodelist_false)


class IfGroupPermNode(template.Node):
    child_nodelists = ('nodelist_true', 'nodelist_false')

    def __init__(self, group_obj, perm_id, nodelist_true, nodelist_false):
        self.group_obj, self.perm_id = group_obj, perm_id
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false

    def __repr__(self):
        return "<IfGroupPermNode>"

    def render(self, context):
        group_obj = self.group_obj.resolve(context, True)
        perm_id = self.perm_id.resolve(context, True)
        perm = Permission.objects.get(id=perm_id)
        perm_str = perm.content_type.app_label + '.' + perm.codename
        if perm in group_obj.permissions.all():
            return self.nodelist_true.render(context)
        return self.nodelist_false.render(context)
