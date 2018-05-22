from django.conf.urls import url
from rango import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^category/(?P<slug>.+)$', views.category_list, name='category_list'),
]