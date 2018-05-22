from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from rango.models import Category,Page


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
