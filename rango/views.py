from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime


def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def visitor_cookie_handler(request):
    visit_cookie = int(request.session.get('visits', '1'))
    last_visit_cookie = request.session.get('last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')
    if (datetime.now()-last_visit_time).seconds > 3:
        visits = visit_cookie+1
        last_visit = str(datetime.now())
    else:
        visits = visit_cookie
        last_visit = last_visit_cookie
    request.session['visits'] = visits
    request.session['last_visit'] = last_visit
    print request.session['visits'],request.session['last_visit']


def index(request):
    request.session.set_test_cookie()
    #context_dict= {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    response = render(request, 'rango/index.html', context=context_dict)

    return response


def test(request):
    return render(request, 'rango/test.html')


def about(request):
    #if request.session.test_cookie_worked():
    #    print "TEST COOKIE WORKED!"
    #request.session.delete_test_cookie()
    return render(request, 'rango/about.html')


def register(request):
    registered = False
    user_form = UserForm()
    userprofile_form = UserProfileForm()
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and userprofile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.is_active = True
            user.is_staff = True
            user.save()

            userprofile = userprofile_form.save(commit=False)
            userprofile.user = user
            if 'picture' in request.FILES:
                userprofile.picture = request.FILES['picture']
            userprofile.save()
            registered = True
        else:
            print user_form.errors,userprofile_form.errors
    context_dict = {'user_form': user_form,
                    'userprofile_form': userprofile_form, 'registered': registered}
    return render(request, 'rango/register.html', context=context_dict)


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'rango/login.html', {})


@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")


@login_required
def user_logout(request):
    if request.user.is_authenticated():
        logout(request)
        return HttpResponseRedirect(reverse('index'))


def category_list(request, slug):
    try:
        categroy=Category.objects.get(slug=slug)
        page_list=Page.objects.filter(category=categroy)
        context_dict = { 'pages': page_list, 'category': categroy,'act_cat':categroy}
    except Category.DoesNotExist:
        context_dict = {'pages': None, 'category': None}
    return render(request, 'rango/category_list.html', context=context_dict)


def add_category(request):
    form=CategoryForm()
    if request.method == 'POST':
        form=CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    return render(request,'rango/add_category.html',{'form':form})


def add_page(request, slug):
    form = PageForm()
    try:
        category = Category.objects.get(slug=slug)
    except Category.DoesNotExist:
        return HttpResponse('category not exist!')
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.category = category
            form.views = 0
            form.save()
            return category_list(request,slug)
        else:
            print(form.errors)
    return render(request, 'rango/add_page.html', {'form': form,'category':category})