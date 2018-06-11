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
from django.contrib.auth.models import User
from rango.models import Province,City,District,Town,Village
import json


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


def user_can_like(request):
    last_visit_cookie = request.session.get('last_visit_like', str(datetime.now()))
    last_visit_like = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')
    print (datetime.now()-last_visit_like).seconds
    if (datetime.now()-last_visit_like).seconds > 300:
        request.session['last_visit_like'] = str(datetime.now())
        return True
    request.session['last_visit_like'] = last_visit_cookie
    return False


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


def test2(request):
    return render(request, 'rango/test2.html')


def about(request):
    #if request.session.test_cookie_worked():
    #    print "TEST COOKIE WORKED!"
    #request.session.delete_test_cookie()
    return render(request, 'rango/about.html')


@login_required
def del_page(request,slug):
    try:
        page = Page.objects.get(title=slug)
        page.delete()
        return HttpResponse(slug+' delete ok!')

    except :

        return HttpResponse(slug+' is not exist!')



@login_required
def like_category(request):
    cat_id = None
    if request.method == 'GET':
        cat_id = request.GET['category_id']

    likes = 0

    if cat_id:
        cat = Category.objects.get(id=int(cat_id))
        if cat:
            likes = cat.likes + 1
            cat.likes = likes
            cat.save()

    return HttpResponse(likes)


def suggest_category(request):
    if request.method == 'GET':
        suggest_str=request.GET['suggest_str']
        suggest_cats=Category.objects.filter(name__icontains=suggest_str)
        response=render(request, 'rango/suggest_cats.html', {'suggest_cats' : suggest_cats})
        print response
        return response
    return HttpResponse('')


def testajax(request):
    if request.method == 'POST':
        username=request.GET['username']
        password = request.GET['password']
        print username, password
        return HttpResponse(username+' '+password)
    return render(request,'rango/testajax.html')


def testajax2(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        if username:
            print 'True'
            print 'hello:'+str(User.objects.get(username=username))
            user = User.objects.get(username=username)
            if user:
                print user.email
                return HttpResponse(user.email)
            else:
                return HttpResponse(username +' is not exist')
        else:
            return HttpResponse('input is null')
    return render(request, 'rango/testajax2.html')


def testjs(request):
    return render(request, 'rango/testjs.html')


def testxss(request):
    if request.method == "POST":
        return HttpResponse('<html><head></head><body>'+request.POST['test']+'</body></html>')
    return render(request,'rango/testxss.html')


def testxss2(request):
    if request.method == "POST":
        return HttpResponse(request.POST['test'])
    return render(request, 'rango/testxss2.html')


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


@login_required
def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    return render(request,'rango/add_category.html',{'form':form})


def testselect(request):
    return render(request, 'rango/testselect.html')


def testjquery(request):
    return  render(request,'rango/testjquery.html')


def get_provinces(request):
    provinces = Province.objects.all()
    provinces_list = []
    for province in provinces:
        provinces_list.append({'id': province.id, 'name': province.name})
    return HttpResponse(json.dumps(provinces_list))


def get_cities(request, province_id):
    cities = City.objects.filter(province_id=province_id)
    cities_list = []
    for city in cities:
        cities_list.append({'id': city.id, 'name': city.name})
    return HttpResponse(json.dumps(cities_list))


def get_districts(request, city_id):
    districts = District.objects.filter(city_id=city_id)
    districts_list = []
    for district in districts:
        districts_list.append({'id': district.id, 'name': district.name})
    return HttpResponse(json.dumps(districts_list))


def get_towns(request, district_id):
    towns = Town.objects.filter(district_id=district_id)
    towns_list = []
    for town in towns:
        towns_list.append({'id': town.id, 'name': town.name})
    return HttpResponse(json.dumps(towns_list))


def get_villages(request, town_id):
    villages = Village.objects.filter(town_id=town_id)
    villages_list = []
    for village in villages:
        villages_list.append({'id': village.id, 'name': village.name})
    return HttpResponse(json.dumps(villages_list))


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
    return render(request, 'rango/add_page.html', {'form': form, 'category':category})