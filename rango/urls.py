from django.conf.urls import url
from rango import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/', views.about, name='about'),
    url(r'^category/(?P<slug>[\w\-]+)$', views.category_list, name='category_list'),
    url(r'^add_category/$', views.add_category, name='add_category'),
    url(r'^(?P<slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
]