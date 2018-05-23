from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm

def index(request):
    #context_dict= {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}
    category_list = Category.objects.order_by('-likes')[:6]
    context_dict = {'categories': category_list }
    return render(request, 'rango/index.html', context=context_dict)


def category_list(request,slug):
    try:
        categroy=Category.objects.get(slug=slug)
        page_list=Page.objects.filter(category=categroy)
        context_dict = { 'pages': page_list, 'category': categroy}
    except Category.DoesNotExist:
        context_dict = {'pages': None, 'category': None}
    return render(request, 'rango/category_list.html', context=context_dict)


def about(request):
    return render(request, 'rango/about.html')


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