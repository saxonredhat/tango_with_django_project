# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from blog.models import *
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
from image_cropping.utils import get_backend
from easy_thumbnails.files import get_thumbnailer
from markdown import markdown
from django.utils import timezone
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


def canvas(request):
    return render(request,'blog/canvas.html')


def index(request):
    return render(request, 'blog/index.html')


def about(request):
    return render(request, 'blog/about.html')


def testajax(request):
    return render(request, 'blog/testajax.html')

def testdiv(reqeust):
    return  render(reqeust,'blog/testdiv.html')

def articles_list(request):
    articles = Article.objects.all().order_by('-pulished_date')
    tag_name=request.GET.get('tag','noexist')
    tag_str=''
    if tag_name != 'noexist':
        tag=Tag.objects.filter(name=tag_name)
        if tag:
            articles = Article.objects.filter(tags__in=tag).order_by('-pulished_date')
            tag_str = tag_name
        else:
            articles = Article.objects.all().order_by('-pulished_date')
    else:
        articles = Article.objects.all().order_by('-pulished_date')
    paginator = Paginator(articles, 8)
    page = request.GET.get('page', 1)
    try:
        articles_list = paginator.page(page)
    except PageNotAnInteger:
        articles_list = paginator.page(1)
    except EmptyPage:
        articles_list = paginator.page(paginator.num_pages)
    return render(request, 'blog/articles_list.html',{'articles': articles_list,'tag':tag_str,'current_url':'articles_list'})


def article_detail(request, article_id):
    comment_form = CommentForm()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            article = Article.objects.get(id=article_id)
            comment.user = request.user
            comment.article = article
            comment.published_date = datetime.now()
            comment.save()
            return HttpResponseRedirect(reverse('article_detail',
                                                kwargs={'article_id':article_id}))
    try:
        article = Article.objects.get(id=article_id)
        comments = Comment.objects.filter(article=article)
        # 增加阅读次数
        article.views = article.views + 1
        article.save()
    except:
        article = None
        comments = None
    context_dict = {'article': article, 'comments': comments,
                  'comment_form':comment_form
                  }
    return render(request, 'blog/article_detail.html', context_dict)



def comment_list(request, article_id):
    try:
        article = Article.objects.get(id=article_id)
        comments = Comment.objects.filter(article=article)
        order = 'asc' if request.GET.get('order','asc') == 'asc' else 'desc'
        if order == 'desc':
            comments=sorted(comments,key=lambda c:c.published_date,reverse=True)
        return render(request,'blog/comment_list.html',{'comments':comments,'article': article,'order': order})
    except Exception, e:
        print Exception, ":", e
        return HttpResponse('article not exist')


#@login_required
def article_add_comment(request, article_id):
    #对ajax请求不使用装饰器login_required
    try:
        user=User.objects.get(id=request.user.id)
        if user:
            #获取文章
            article=Article.objects.get(id=article_id)
            #获取评论的内容
            if request.method == 'POST':
                content = request.POST.get('content')
                comment = Comment(content=content,user=request.user,article=article,published_date =datetime.now(tz=timezone.utc))
                comment.save()
                comment_layer=article.comment_set.all().count()
                print comment_layer
                return render(request, 'blog/comments_of_article.html',{'comment': comment,'article': article,'comment_layer': comment_layer})
            return HttpResponse('403 request method')
    except Exception,e:
        print Exception, ":", e
        return HttpResponse('403')



@login_required
def comment_user(request,comment_id,user_id):
    if request.method == 'POST':
        comment = Comment.objects.get(id=comment_id)
        user = User.objects.get(id=user_id)
        comment_user=request.POST.get('comment_user')
        article_id=request.GET.get('article_id')
        published_date=datetime.now(tz=timezone.utc)
        c=Comment(comt=comment,user=user,published_date=published_date,content=comment_user)
        c.save()
        return HttpResponseRedirect(reverse('article_detail',kwargs={'article_id':article_id}))
    return HttpResponseRedirect(reverse('index'))


#@login_required
def comment_user_first(request,comment_id,article_id):
    # 对ajax请求不使用装饰器login_required
    try:
        user = User.objects.get(id=request.user.id)
        if user:
            if request.method == 'POST':
                user = request.user
                comment = Comment.objects.get(id=comment_id)
                article = Article.objects.get(id=article_id)
                comment_user_content = request.POST.get('comment_user_content')
                published_date = datetime.now(tz=timezone.utc)
                comment_user_new = Comment(comt=comment, user=user, published_date=published_date,
                                           content=comment_user_content)
                comment_user_new.save()
                return render(request, 'blog/comments_of_user.html',
                              {'comment_user': comment_user_new, 'article': article, 'first_second': 'first'})
            return HttpResponse('403 request method')
    except Exception,e:
        print Exception, ":", e
        return HttpResponse('403')



#@login_required
def comment_user_second(request, comment_id, article_id):
    # 对ajax请求不使用装饰器login_required
    try:
        user = User.objects.get(id=request.user.id)
        if user:
            if request.method == 'POST':
                comment = Comment.objects.get(id=comment_id)
                user = request.user
                article = Article.objects.get(id=article_id)
                comment_user_content = request.POST.get('comment_user_content')
                article_id = request.GET.get('article_id')
                published_date = datetime.now(tz=timezone.utc)
                comment_user_new = Comment(comt=comment, user=user, published_date=published_date,
                                           content=comment_user_content)
                comment_user_new.save()
                return render(request, 'blog/comments_of_user.html',
                              {'comment_user': comment_user_new, 'article': article, 'first_second': 'second'})
            return HttpResponse('403 request method')
    except Exception, e:
        print Exception, ":", e
        return HttpResponse('403')


@login_required
def comment_delete(request,comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
        if request.user == comment.user:
            comment.delete()
            return HttpResponse('delete')
        else:
            return HttpResponse('403')
    except:
        return HttpResponse('error')


def like_user(request,user_id):
    try:
        user = User.objects.get(id=request.user.id)
        if user:
            like_user=User.objects.filter(id=user_id)[0]
            like=Like.objects.filter(like_user=like_user)
            if like or not like_user:
                return HttpResponse('error')
            like=Like(like_user=like_user,user_id=request.user.id)
            like.save()
            return HttpResponse('like_user')
    except Exception, e:
        print Exception, ":", e
        return HttpResponse('403')

def like_article(request,article_id):
    try:
        user = User.objects.get(id=request.user.id)
        if user:
            like_article = Article.objects.filter(id=article_id)[0]
            like = Article.objects.filter(like_article=like_article)
            if like or not like_article:
                return HttpResponse('error')
            like = Like(like_article=like_article,user_id=request.user.id)
            like.save()
            return HttpResponse('like_article')
    except Exception, e:
        print Exception, ":", e
        return HttpResponse('403')


#点赞文章评论view处理
def like_comment(request,comment_id):
    try:
        user = User.objects.get(id=request.user.id)
        if user:
            like_comment = Comment.objects.filter(id=comment_id)[0]
            like = Like.objects.filter(like_comment=like_comment,user_id=request.user.id)
            if like or not like_comment:
                print 'exist'
                return HttpResponse('exist')
            like = Like(like_comment=like_comment,user_id=request.user.id)
            like.save()
            print 'like_comment'
            return HttpResponse('like_comment')
    except Exception, e:
        print Exception, ":", e
        return HttpResponse('403')


#点赞文章view处理
def like_article(request,article_id):
    try:
        user = User.objects.get(id=request.user.id)
        if user:
            like_article = Article.objects.filter(id=article_id)[0]
            like = Like.objects.filter(like_article=like_article,user_id=request.user.id)
            if like or not like_article:
                print 'exist'
                return HttpResponse('exist')
            like = Like(like_article=like_article,user_id=request.user.id)
            like.save()
            print 'like_article'
            return HttpResponse('like_article')
    except Exception, e:
        print Exception, ":", e
        return HttpResponse('403')


#点赞用户view处理
def like_user(request,user_id):
    try:
        user = User.objects.get(id=request.user.id)
        if user:
            like_user = User.objects.filter(id=user_id)[0]
            like = Like.objects.filter(like_user=like_user,user_id=request.user.id)
            if like or not like_user:
                print 'exist'
                return HttpResponse('exist')
            like = Like(like_user=like_user,user_id=request.user.id)
            like.save()
            print 'like_user'
            return HttpResponse('like_user')
    except Exception, e:
        print Exception, ":", e
        return HttpResponse('403')

#添加关注用户、取消关注用户
def user_follow(request,user_id):
    try:
        user = User.objects.get(id=request.user.id)
        if user:
            try:
                followee_user = User.objects.get(id=user_id)
            except Exception, e:
                print Exception, ":", e
                return HttpResponse('noexist')
            follow = Follow.objects.filter(followee=followee_user,follower=request.user)
            if follow:
                follow[0].delete()
                return HttpResponse('unfollow')
            else:
                follow = Follow(followee=followee_user,follower=request.user)
                follow.save()
                return HttpResponse('follow')
    except Exception, e:
        print Exception, ":", e
        return HttpResponse('403')


def user_followers(request,user_id):
    try:
        user = User.objects.get(id=user_id)
        followers=[]
        for follow in user.followees.all():
            followers.append(follow.follower)
        paginator = Paginator(followers, 8)
        page = request.GET.get('page', 1)
        try:
            followers_list = paginator.page(page)
        except PageNotAnInteger:
            followers_list = paginator.page(1)
        except EmptyPage:
            followers_list = paginator.page(paginator.num_pages)
        followers_list.page_type='followers'
        return render(request,'blog/user_followers.html',{'followers':followers_list})
    except Exception, e:
        print Exception, ":", e
        return HttpResponse('noexist')


def user_followees(request,user_id):
    try:
        user = User.objects.get(id=user_id)
        followees = []
        for follow in user.followers.all():
            followees.append(follow.followee)
        paginator = Paginator(followees, 8)
        page = request.GET.get('page', 1)
        try:
            followees_list = paginator.page(page)
        except PageNotAnInteger:
            followees_list = paginator.page(1)
        except EmptyPage:
            followees_list = paginator.page(paginator.num_pages)
        followees_list.page_type = 'followees'
        return render(request, 'blog/user_followees.html', {'followees': followees_list})
    except Exception, e:
        print Exception, ":", e
        return HttpResponse('noexist')


def user_articles(request,user_id):
    try:
        user = User.objects.get(id=user_id)
        tag_name = request.GET.get('tag', 'noexist')
        tag_str = ''
        if tag_name != 'noexist':
            tag = Tag.objects.filter(name=tag_name)
            if tag:
                articles = Article.objects.filter(tags__in=tag, author=user).order_by('-pulished_date')
                tag_str = tag_name
            else:
                articles = Article.objects.filter(author=user).order_by('-pulished_date')
        else:
            articles = Article.objects.filter(author=user).order_by('-pulished_date')
        paginator = Paginator(articles, 8)
        page = request.GET.get('page', 1)
        try:
            articles_list = paginator.page(page)
        except PageNotAnInteger:
            articles_list = paginator.page(1)
        except EmptyPage:
            articles_list = paginator.page(paginator.num_pages)
        return render(request,'blog/user_articles.html',{'articles':articles_list,'get_user':user,'current_url':'user_zone'})
    except Exception, e:
        print Exception, ":", e
        return HttpResponse('noexist')

#取消关注用户
def user_un_follower(request,user_id):
    pass


@login_required
def article_add(request):
    form = ArticleForm()
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            for t in form.cleaned_data.get('tags').split(';'):
                try:
                    tag=Tag.objects.get(name=t)
                except Exception, e:
                    print Exception, ":", e
                    tag=Tag(name=t)
                    tag.save()
                article.tags.add(tag)
            return HttpResponseRedirect(reverse('index'))
    return render(request, 'blog/article_add.html', {'form': form})


@login_required
def article_update_list(request):
    current_user=request.user
    articles = Article.objects.filter(author=current_user)
    return render(request, 'blog/article_update_list.html', {'articles': articles})


@login_required
#@permission_required('blog.update_article')
def article_update(request,article_id):
    current_user=request.user
    try:
        article = Article.objects.get(id=article_id)
        if article.author != current_user:
            messages.error(request, '无权编辑其他用户的文章.')
            return HttpResponseRedirect(reverse('article_update_list'))
    except:
        messages.error(request, '请求的对象错误.')
        return HttpResponseRedirect(reverse('article_update_list'))
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article.title=form.cleaned_data.get('title')
            article.type = form.cleaned_data.get('type')
            article.content = form.cleaned_data.get('content')
            article.category = form.cleaned_data.get('category')
            #删除之前的tags
            for tag in article.tags.all():
                try:
                    article.tags.remove(tag)
                except:
                    pass
            for t in form.cleaned_data.get('tags').split(';'):
                try:
                    tag=Tag.objects.get(name=t)
                except Exception, e:
                    print Exception, ":", e
                    tag=Tag(name=t)
                    tag.save()
                article.tags.add(tag)
            article.save()
            return HttpResponseRedirect(reverse('article_update_list'))
    else:
        title= article.title
        type = article.type
        content = article.content
        category = article.category
        tag_list = [ t.name for t in article.tags.all()]
        tags=';'.join(tag_list)
        article_dict={'title':title, 'type':type,
                      'content':content, 'category':category,
                      'tags':tags}
        form = ArticleForm(article_dict)
    return render(request, 'blog/article_update.html', {'form': form})


@login_required
#@permission_required('blog.del_article')
def article_delete_list(request):
    current_user = request.user
    articles = Article.objects.filter(author=current_user)
    return render(request, 'blog/article_delete_list.html', {'articles': articles})


@login_required
#@permission_required('blog.add_article')
def article_delete(request, article_id):
    current_user = request.user
    try:
        article = Article.objects.get(id=article_id)
        title = article.title
        if article.author == current_user:
            Article.objects.get(id=article_id).delete()
        else:
            messages.error(request, '无权删除其他用户的文章.')
            return HttpResponseRedirect(reverse('article_delete_list'))
        messages.success(request, '文章'+title+'删除成功.')
    except:
        messages.error(request, '文章删除失败.')
    return HttpResponseRedirect(reverse('article_delete_list'))


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
    user_info_form = UserInfoForm()
    if request.method == 'POST':
        user_register_form = UserRegisterForm(request.POST)
        user_info_form = UserInfoForm(request.POST)
        if user_register_form.is_valid() and user_info_form.is_valid():
            username = user_register_form.cleaned_data.get('username')
            email = user_register_form.cleaned_data.get('email')
            password = user_register_form.cleaned_data.get('password1')
            user = User.objects.create_user(username=username, password=password, email=email)
            user.is_active = False
            user.save()
            user_info=user_info_form.save(commit=False)
            user_info.user=user
            user_info.save()
            token = token_confirm.generate_validate_token(username)
            text = "\n".join([u'{0},欢迎加入我的博客'.format(username), u'请访问该链接，完成用户验证:',
                                 '/'.join(['http://codemax.vicp.io:8888', 'blog/activate', token])])
            send_mail(u'注册用户验证信息', text, 'sys_blog@163.com', [email], fail_silently=False)
            message='恭喜,注册成功!请注意查收邮件激活账号.'
            return render(request,'blog/message.html',{'message':message})
    return render(request, 'blog/user_register.html', {'user_register_form': user_register_form})


@login_required
def user_info(request):
    try:
        user = request.user
    except:
        return HttpResponse('用户id'+str(user_id)+'不存在')
    if request.method == 'POST':
        try:
            #user_form = UserBaseForm(request.POST)
            user_info_form = UserInfoForm(request.POST)
            #print user_info_form.is_valid(),user_form.is_valid()
            print
            if user_info_form.is_valid():
                #user.username = user_form.cleaned_data.get('username')
                #user.email = user_form.cleaned_data.get('email')
                #user.save()
                try:
                    user_info = UserInfo.objects.get(user=user)
                except:
                    user_info = user_info_form.save(commit=False)
                user_info.website=user_info_form.cleaned_data.get('website','')
                user_info.user = user
                print request.FILES
                print 'ok'
                if 'picture' in request.FILES:
                    user_info.picture = request.FILES['picture']
                user_info.save()
        except Exception,e:
            print Exception,e

        return HttpResponseRedirect(reverse('user_info'))
    else:
        username=user.username
        email=user.email
        user_dict={'username':username, 'email': email}
        try:
            user_info=UserInfo.objects.get(user=user)
            website = user_info.website
            picture = user_info.picture
            user_info_dict = {'website': website,'picture':picture}
        except:
            user_info_dict={}
        user_form=UserBaseForm(user_dict)
        user_info_form=UserInfoForm(user_info_dict)
    return render(request,'blog/user_info.html',{'user_form': user_form, 'user_info_form': user_info_form})


def user_zone(request,user_id):
    #判断请求的user_id对应的用户是否存在
    try:
        get_user = User.objects.get(id=user_id)
    except:
        return HttpResponse('用户id'+str(user_id)+'不存在')
    #获取访问记录
    #初始化字典context_dict
    context_dict={}
    #赋值请求的用户对象
    context_dict['get_user']=get_user
    visit_history = None
    #判断用户不是匿名并且不是该访问页面的用户自己的页面，保存用户的访问记录
    if not request.user.is_anonymous() and request.user != get_user:
        try:
            #如果当前用户访问过该页面，则更新访问时间
            visit_history = VisitHistory.objects.get(interviewee=get_user,visitor=request.user)
            visit_history.accessed_at = datetime.now(tz=timezone.utc)
            visit_history.save()
        except Exception, e:
            print Exception, ":", e
        if not visit_history:
            # 如果当前用户未访问过该页面，则增加访问记录
            visit_history = VisitHistory(interviewee=get_user, visitor=request.user)
            visit_history.save()
    #热门文章
    articles_hot = Article.objects.filter(author=get_user).order_by('-views')
    context_dict['articles_hot'] = articles_hot
    #获取请求的页面类型，如果没有，默认articles页面
    page_type = request.GET.get('page_type', 'articles')
    #如果page_type为articles，获取文章列表
    if page_type == 'articles':
        tag_name = request.GET.get('tag', 'noexist')
        tag_str = ''
        if tag_name != 'noexist':
            tag = Tag.objects.filter(name=tag_name)
            if tag:
                articles = Article.objects.filter(tags__in=tag,author=get_user).order_by('-pulished_date')
                tag_str = tag_name
            else:
                articles = Article.objects.filter(author=get_user).order_by('-pulished_date')
        else:
            articles = Article.objects.filter(author=get_user).order_by('-pulished_date')
        paginator = Paginator(articles, 6)
        paginator.page_type='articles'
        page = request.GET.get('page', 1)
        try:
            articles_list = paginator.page(page)
        except PageNotAnInteger:
            articles_list = paginator.page(1)
        except EmptyPage:
            articles_list = paginator.page(paginator.num_pages)
        articles_list.page_type = 'articles'
        context_dict['articles'] = articles_list
    # 如果page_type为followers，获取粉丝列表
    elif page_type == 'followers':
        followers = []
        for follow in get_user.followees.all():
            followers.append(follow.follower)
        paginator = Paginator(followers, 8)
        paginator.page_type = 'followers'
        page = request.GET.get('page', 1)
        try:
            followers_list = paginator.page(page)
        except PageNotAnInteger:
            followers_list = paginator.page(1)
        except EmptyPage:
            followers_list = paginator.page(paginator.num_pages)
        followers_list.page_type = 'followers'
        context_dict['followers'] = followers_list
    # 如果page_type为followees，获取关注列表
    elif page_type == 'followees':
        followees = []
        for follow in get_user.followers.all():
            followees.append(follow.followee)
        paginator = Paginator(followees, 8)
        page = request.GET.get('page', 1)
        try:
            followees_list = paginator.page(page)
        except PageNotAnInteger:
            followees_list = paginator.page(1)
        except EmptyPage:
            followees_list = paginator.page(paginator.num_pages)
        followees_list.page_type = 'followees'
        context_dict['followees'] = followees_list
    else:
        pass
    #当前页面的url
    context_dict['current_url']='user_zone'
    return render(request, 'blog/user_zone.html', context_dict)


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
    user_form = UserAddForm()
    if request.method == 'POST':
        user_form = UserAddForm(request.POST)
        if user_form.is_valid():
            user_form.save(commit=True)
            return HttpResponseRedirect(reverse('user_manage'))
    return render(request, 'blog/user_add.html', {'user_form': user_form})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def user_active(request,user_id):
    try:
        user=User.objects.get(id=user_id)
        if user.is_active:
            user.is_active = False
        else:
            user.is_active = True
        user.save()
        return HttpResponseRedirect(reverse('user_manage'))
    except:
        return HttpResponse('用户id不存在')


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