from django.conf.urls import url
from rango import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/', views.register, name='register'),
    url(r'^login/', views.user_login, name='login'),
    url(r'^logout/', views.user_logout, name='logout'),
    url(r'^restricted/',views.restricted, name='restricted'),
    url(r'^about/', views.about, name='about'),
    url(r'^category/(?P<slug>[\w\-]+)$', views.category_list, name='category_list'),
    url(r'^add_category/$', views.add_category, name='add_category'),
    url(r'^(?P<slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
    url(r'^test/$', views.test),
]