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
    url(r'^test2/$', views.test2),
    url(r'^like_category/$', views.like_category, name='like_category'),
    url(r'^suggest_category/$', views.suggest_category, name='suggest_category'),
    url(r'^testajax/$', views.testajax, name='testajax'),
    url(r'^testxss/', views.testxss, name='testxss'),
    url(r'^testxss2/', views.testxss2, name='testxss2'),
    url(r'^testjs/', views.testjs, name='testjs'),
    url(r'^testajax2/$', views.testajax2, name='testajax2'),
    url(r'^page/del/(?P<slug>\w+)$', views.del_page, name='del_page'),
    url(r'^testselect/$', views.testselect, name='testselect'),
    url(r'^get_provinces/$', views.get_provinces, name='get_provinces'),
    url(r'^get_cities/(?P<province_id>\d+)$', views.get_cities, name='get_cities'),
    url(r'^get_districts/(?P<city_id>\d+)$', views.get_districts, name='get_districts'),
    url(r'^get_towns/(?P<district_id>\d+)$', views.get_towns, name='get_towns'),
    url(r'^get_villages/(?P<town_id>\d+)$', views.get_villages, name='get_villages'),
    url(r'^testjquery/$', views.testjquery, name='testjquery'),
]