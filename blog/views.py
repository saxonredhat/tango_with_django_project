# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from blog.models import Article,Comment
from blog.forms import *
from datetime import datetime
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group, Permission
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from functools import partial
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from guardian.shortcuts import assign_perm,remove_perm
from itsdangerous import URLSafeTimedSerializer as utsr
from django.conf import settings as django_settings
from django.core.mail import send_mail
from markdown import markdown
import mytools
import base64
import re
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

login_required = partial(login_required, login_url='/blog/login')
permission_required = partial(permission_required, raise_exception=True)
user_passes_test=partial(user_passes_test, login_url='/blog/login')


class Token:
    def __init__(self, security_key):
        self.security_key = security_key
        self.salt = base64.encodestring(security_key)

    def generate_validate_token(self, username):
        serializer = utsr(self.security_key)
        return serializer.dumps(username, self.salt)

    def confirm_validate_token(self, token, expiration=3600):
        serializer = utsr(self.security_key)
        return serializer.loads(token, salt=self.salt, max_age=expiration)

    def remove_validate_token(self, token):
        serializer = utsr(self.security_key)
        return serializer.loads(token, salt=self.salt)

token_confirm = Token(django_settings.SECRET_KEY)



def index(request):
    return render(request, 'blog/index.html')


def about(request):
    return render(request, 'blog/about.html')


def articles_list(request):
    articles = Article.objects.all()
    return render(request, 'blog/articles_list.html',{'articles': articles})


def article_detail(request, article_id):
    try:
        article = Article.objects.get(id=article_id)
        comments = Comment.objects.filter(article=article)
    except:
        article = None
    return render(request, 'blog/article_detail.html', {'article': article, 'comments': comments})


@login_required
@permission_required('blog.add_article')
def add_article(request):
    form = ArticleForm()
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            author = Author.objects.get(id=1)
            article.pulished_date=datetime.now()
            article.author=author
            article.save()
            return HttpResponseRedirect(reverse('index'))
    return render(request, 'blog/add_article.html', {'form': form})


@login_required
@permission_required('blog.add_article')
def update_article(request):
    form = ArticleForm()
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            author=Author.objects.get(id=1)
            article.pulished_date=datetime.now()
            article.author=author
            article.save()
            return HttpResponseRedirect(reverse('index'))
    return render(request, 'blog/add_article.html', {'form': form})


@login_required
@permission_required('blog.add_article')
def delete_article(request):
    form = ArticleForm()
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            author=Author.objects.get(id=1)
            article.pulished_date=datetime.now()
            article.author=author
            article.save()
            return HttpResponseRedirect(reverse('index'))
    return render(request, 'blog/add_article.html', {'form': form})


def user_login(request):
    errors = ''
    next_url = request.GET.get('next', '/blog')
    if request.method == 'POST':
        print 'ok'
        username=request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(next_url)
            errors = '用户没有激活'
        else:
            errors = '用户不存在或者密码错误'
    return render(request, 'blog/user_login.html', {'errors': errors})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def user_register(request):
    user_register_form = UserRegisterForm()
    if request.method == 'POST':
        user_register_form = UserRegisterForm(request.POST)
        if user_register_form.is_valid():
            username = user_register_form.cleaned_data.get('username')
            email = user_register_form.cleaned_data.get('email')
            password = user_register_form.cleaned_data.get('password1')
            user = User.objects.create_user(username=username, password=password, email=email)
            user.is_active = False
            user.save()
            token = token_confirm.generate_validate_token(username)
            text = "\n".join([u'{0},欢迎加入我的博客'.format(username), u'请访问该链接，完成用户验证:',
                                 '/'.join([django_settings.DOMAIN, 'blog/activate', token])])
            send_mail(u'注册用户验证信息', text, 'sys_blog@163.com', [email], fail_silently=False)
            message='恭喜,注册成功!请注意查收邮件激活账号.'
            return render(request,'blog/message.html',{'message':message})
    return render(request, 'blog/user_register.html', {'user_register_form': user_register_form})


def active_user(request, token):
    try:
        username = token_confirm.confirm_validate_token(token)
    except:
        username = token_confirm.remove_validate_token(token)
        users = User.objects.filter(username=username)
        for user in users:
            user.delete()
        return render(request, 'message.html', {'message': u'对不起，验证链接已经过期，请重新<a href=\"' + unicode(django_settings.DOMAIN) + u'/signup\">注册</a>'})
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return render(request, 'message.html', {'message': u"对不起，您所验证的用户不存在，请重新注册"})
    user.is_active = True
    user.save()
    message = u'验证成功，请进行网站 <a href="' + unicode(django_settings.DOMAIN) + u'/blog/login">登录</a>操作'
    return render(request, 'blog/message.html', {'message':message})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def user_manage(request):
    users = User.objects.all()
    return render(request, 'blog/user_manage.html', {'users': users})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def user_add(request):
    user_form = UserForm()
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user_form.save(commit=True)
            return HttpResponseRedirect(reverse('user_manage'))
    return render(request, 'blog/user_add.html', {'user_form': user_form})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def user_update(request, user_id):
    if request.method == 'POST':
        try:
            user = User.objects.get(id=user_id)
        except:
            messages.error(request, '访问用户编辑页面异常.')
            return HttpResponseRedirect(reverse('index'))
        user_form = UserEditForm(request.POST)
        if user_form.is_valid():
            password=user_form.cleaned_data.get("password1")
            if password:
                user.set_password(password)
            user.email=user_form.cleaned_data.get("email")
            user.save()
            return HttpResponseRedirect(reverse('user_manage'))
    else:
        try:
            user = User.objects.get(id=user_id)
            user_info = {'email': user.email}
            user_form = UserEditForm(user_info)
        except:
            messages.error(request, '访问用户编辑页面异常.')
            return HttpResponseRedirect(reverse('index'))
    return render(request, 'blog/user_update.html', {'user_form': user_form,'username': user.username})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def user_delete(request,user_id):
    try:
        User.objects.get(id=user_id).delete()
        messages.success(request, '用户删除成功.')
    except:
        messages.error(request, '用户删除失败.')
    return HttpResponseRedirect(reverse('user_manage'))


@login_required
@user_passes_test(lambda u: u.is_superuser)
def group_manage(request):
    groups = Group.objects.all()
    return render(request, 'blog/group_manage.html', {'groups': groups})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def group_add(request):
    group_form = GroupForm()
    if request.method == 'POST':
        group_form = GroupForm(request.POST)
        if group_form.is_valid():
            group_form.save(commit=True)
            return HttpResponseRedirect(reverse('group_manage'))
    return render(request, 'blog/group_add.html', {'group_form': group_form})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def group_update(request, group_id):
    if request.method == 'POST':
        try:
            user = Group.objects.get(id=group_id)
        except:
            messages.error(request, '访问用户编辑页面异常.')
            return HttpResponseRedirect(reverse('index'))
        user_form = UserEditForm(request.POST)
        if user_form.is_valid():
            password=user_form.cleaned_data.get("password1")
            if password:
                user.set_password(password)
            user.email=user_form.cleaned_data.get("email")
            user.save()
            return HttpResponseRedirect(reverse('user_manage'))
    else:
        try:
            group = Group.objects.get(id=group_id)
            user_for_group=group.user_set.all()
            users=User.objects.all()
        except:
            messages.error(request, '访问用户编辑页面异常.')
            return HttpResponseRedirect(reverse('index'))
    return render(request, 'blog/group_update.html', {'group': group,'users': users,'user_for_group': user_for_group})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def group_delete(request, group_id):
    try:
        Group.objects.get(id=group_id).delete()
        messages.success(request, '用户组删除成功.')
    except:
        messages.error(request, '用户组删除失败.')
    return HttpResponseRedirect(reverse('group_manage'))


@login_required
@user_passes_test(lambda u: u.is_superuser)
def remove_user_from_group(request,user_id,group_id):
    try:
        group = Group.objects.get(id=group_id)
        user = User.objects.get(id=user_id)
        if group and user:
            print group,user
            user.groups.remove(group)
            messages.success(request, '从用户组移除成功.')
    except:
        messages.error(request, '用户从组移除失败.')
    return HttpResponseRedirect(reverse('group_update', kwargs={"group_id": group_id}))


@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_user_to_group(request, user_id, group_id):
    try:
        group = Group.objects.get(id=group_id)
        user = User.objects.get(id=user_id)
        if group and user:
            user.groups.add(group)
            messages.success(request, '添加到用户组成功.')
    except:
        messages.error(request, '用户添加到用户组失败.')
    return HttpResponseRedirect(reverse('group_update', kwargs={"group_id": group_id}))


@login_required
@user_passes_test(lambda u: u.is_superuser)
def perm_manage(request):
    perms = Permission.objects.order_by('id')
    perms = [perm for perm in perms if mytools.str_contain_chinese(perm)]
    paginator= Paginator(perms, 8)
    page = request.GET.get('page', 1)
    try:
        perms_list = paginator.page(page)
    except PageNotAnInteger:
        perms_list = paginator.page(1)
    except EmptyPage:
        perms_list = paginator.page(paginator.num_pages)
    return render(request, 'blog/perm_manage.html', {'perms': perms_list})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def perm_add(request):
    permission_form = PermissionForm()
    if request.method == 'POST':
        permission_form = PermissionForm(request.POST)
        if permission_form.is_valid():
            try:
                perm = permission_form.save(commit=False)
                app_label, model = permission_form.cleaned_data.get('app_label_model').split('-')
                content_type = ContentType.objects.get(app_label=app_label,model=model)
                perm.content_type = content_type
                perm.save()
                messages.success(request, '添加权限成功.')
            except:
                messages.error(request, '添加权限失败.')
            return HttpResponseRedirect(reverse('perm_manage'))
    return render(request, 'blog/perm_add.html', {'permission_form': permission_form})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def perm_delete(request):
    pass


@login_required
@user_passes_test(lambda u: u.is_superuser)
def perm_update(request):
    pass


@login_required
@user_passes_test(lambda u: u.is_superuser)
def user_perm(request,user_id):
    myuser=User.objects.get(id=user_id)
    perms = Permission.objects.order_by('id')
    perms = [perm for perm in perms if mytools.str_contain_chinese(perm)]
    paginator = Paginator(perms, 8)
    page = request.GET.get('page', 1)
    try:
        perms_list = paginator.page(page)
    except PageNotAnInteger:
        perms_list = paginator.page(1)
    except EmptyPage:
        perms_list = paginator.page(paginator.num_pages)
    return render(request, 'blog/user_perm.html', {'myuser':myuser,'myperms': perms_list})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def user_remove_perm(request, user_id, perm_id):
    user = User.objects.get(id=user_id)
    perm = Permission.objects.get(id=perm_id)
    perm_code = perm.content_type.app_label + '.' + perm.codename
    remove_perm(perm_code,user)
    page = request.GET.get('page',1)
    return HttpResponseRedirect(reverse('user_perm',kwargs={'user_id':user_id}) + "?page="+page)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def user_add_perm(request, user_id, perm_id):
    user = User.objects.get(id=user_id)
    perm = Permission.objects.get(id=perm_id)
    perm_code = perm.content_type.app_label + '.' + perm.codename
    assign_perm(perm_code, user)
    page = request.GET.get('page',1)
    return HttpResponseRedirect(reverse('user_perm',kwargs={'user_id':user_id}) + "?page="+page)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def group_perm(request, group_id):
    mygroup=Group.objects.get(id=group_id)
    perms = Permission.objects.order_by('id')
    perms = [perm for perm in perms if mytools.str_contain_chinese(perm)]
    paginator = Paginator(perms, 8)
    page = request.GET.get('page', 1)
    try:
        perms_list = paginator.page(page)
    except PageNotAnInteger:
        perms_list = paginator.page(1)
    except EmptyPage:
        perms_list = paginator.page(paginator.num_pages)
    return render(request, 'blog/group_perm.html', {'mygroup': mygroup, 'myperms': perms_list})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def group_remove_perm(request, group_id, perm_id):
    group = Group.objects.get(id=group_id)
    perm = Permission.objects.get(id=perm_id)
    perm_code = perm.content_type.app_label + '.' + perm.codename
    remove_perm(perm_code, group)
    page = request.GET.get('page', 1)
    return HttpResponseRedirect(reverse('group_perm', kwargs={'group_id': group_id}) + "?page="+page)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def group_add_perm(request, group_id, perm_id):
    group = Group.objects.get(id=group_id)
    perm = Permission.objects.get(id=perm_id)
    perm_code = perm.content_type.app_label + '.' + perm.codename
    assign_perm(perm_code, group)
    page = request.GET.get('page', 1)
    return HttpResponseRedirect(reverse('group_perm', kwargs={'group_id': group_id}) + "?page="+page)


def http_403(request):
    return render(request, 'blog/http_403.html')


def http_404(request):
    return render(request, 'blog/http_403.html')