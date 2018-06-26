# -*- coding:utf-8 -*-
from django import template
from django.contrib.auth.models import User,Group,Permission
from django.template.base import TemplateSyntaxError,NodeList
from blog.models import *
from markdown import markdown
from django.shortcuts import render
#from guardian.core import ObjectPermissionChecker
from django.conf import settings
from django.utils.encoding import force_text, force_unicode
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter
from django.db.models import Q
import re
import datetime
register = template.Library()
import sys
sys.setrecursionlimit(5000)

@register.filter
def del_html_tag(content):
    return re.sub(r'<[^>]*>', '', content)


@register.filter
def my_markdown(content):
    return markdown(content)


@register.filter(is_safe=True)
@stringfilter
def markdown2(value):
    try:
        import markdown
    except ImportError:
        if settings.DEBUG:
            raise template.TemplateSyntaxError("Error in 'markdonw' filter: The Python markdown2 library isn't install.")
        return force_text(value)
    else:
        return mark_safe(markdown.markdown(value,
                                       extensions=['markdown.extensions.fenced_code', 'markdown.extensions.codehilite'],
                                       safe_mode=True,
                                       enable_attributes=False))


@register.filter
def cut_name(content):
    return content[0:5]


@register.filter
def cut_name_dot(content):
    if len(content) > 5:
        return '...'
    return ''


@register.filter
def convert_html_white(content):
    return "&nbsp;".join(content.split(' '))


@register.filter
def string_safe(content):
    return content


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
def last_message(send_user, receive_user):
    try:
        message = Message.objects.filter(send_user=send_user,receive_user=receive_user).order_by('-created_at')[0]
    except Exception, e:
        print Exception, e
        return ''
    return message


@register.simple_tag
def get_follow_time(follower,followee):
    try:
        follow_time=Follow.objects.get(follower=follower,followee=followee).created_at
    except Exception, e:
        print Exception, e
        return ''
    return follow_time.strftime("%Y-%m-%d %H:%M:%S")


@register.simple_tag
def format_time(f_time):
    now_t = datetime.datetime.now()
    yestoday_str= datetime.datetime.strftime(now_t - datetime.timedelta(1), '%Y-%m-%d')
    current_year_start_time = datetime.datetime.strptime(str(now_t.year)+'-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    yestoday_start_time = datetime.datetime.strptime(yestoday_str+' 00:00:00', '%Y-%m-%d %H:%M:%S')
    today_start_time= datetime.datetime.strptime(now_t.strftime("%Y-%m-%d")+' 00:00:00', '%Y-%m-%d %H:%M:%S')
    current_year_seconds = (now_t-current_year_start_time).total_seconds()
    yestoday_seconds = (now_t-yestoday_start_time).total_seconds()
    today_seconds = (now_t-today_start_time).total_seconds()
    total_seconds = (now_t-f_time).total_seconds()
    print
    if total_seconds > current_year_seconds:
        return f_time.strftime("%Y年%m月%d日 %H:%M:%S")
    elif total_seconds > yestoday_seconds:
        return f_time.strftime("%m月%d日 %H:%M:%S")
    elif total_seconds > today_seconds:
        return f_time.strftime("昨天 %H:%M:%S")
    else:
        return f_time.strftime("今天 %H:%M:%S")


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


#获取用户消息数
@register.simple_tag
def get_user_messages_count(user):
    counts = 0
    # 获取用户关注数
    follow_count = sum([1 for f in user.followees.all() if f.is_read == 0])
    # 获取未读的收藏数量
    favorite_count = Favorite.objects.filter(article__in=user.article_set.all(), is_read=0).count()
    # 获取未读的点赞数量
    like_count = Like.objects.filter(
        Q(like_article__in=user.article_set.all(), is_read=0) | Q(like_comment__in=user.comment_set.all(),
                                                                  is_read=0)).filter(~Q(user_id=user.id)).count()
    # 获取文章的评论数
    article_comment_count = Comment.objects.filter(article__in=user.article_set.all(), is_read=0).filter(
        ~Q(user=user)).count()

    # 获取用户评论的回复数
    comment_replies_counts = Comment.objects.filter(comt__in=user.comment_set.all(), is_read=0).filter(
        ~Q(user=user)).count()

    counts = follow_count+favorite_count+like_count+article_comment_count+comment_replies_counts
    if counts > 0:
        return counts
    return ''



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


#获取用户的对象
@register.assignment_tag
def get_user(user_id):
    try:
        user = User.objects.get(id=user_id)
        return user
    except Exception, e:
        print Exception, e
        return ''


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
