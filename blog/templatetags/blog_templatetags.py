from django import template
from django.contrib.auth.models import User,Group,Permission
from django.template.base import TemplateSyntaxError,NodeList
from blog.models import Comment
from markdown import markdown
#from guardian.core import ObjectPermissionChecker
import re
#import datetime
register = template.Library()


@register.filter
def del_html_tag(content):
    return re.sub(r'<[^>]*>', '', content)


@register.filter
def my_markdown(content):
    return markdown(content)


@register.simple_tag
def comment_by_comment(comment_id):
    counts = 0
    comment = Comment.objects.get(id=comment_id)
    if comment.comment_set.all().count():
        for c in comment.comment_set.all():
            counts += 1
            counts += comment_by_comment(c.id)
    else:
        return 0
    return counts



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
