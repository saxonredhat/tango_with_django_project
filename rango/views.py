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
    categroy=Category.objects.filter(slug=slug)[0]
    page_list=Page.objects.filter(category=categroy)
    context_dict = { 'pages': page_list }
    return render(request, 'rango/category_list.html', context=context_dict)
