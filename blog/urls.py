from django.conf.urls import url
from blog import views, upload
from django.views.static import serve
from tango_with_django_project import settings

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^articles_list/$', views.articles_list, name='articles_list'),
    url(r'^article_detail/(?P<article_id>\d+)$', views.article_detail, name='article_detail'),
    url(r'^add_article/$', views.add_article, name='add_article'),
    url(r'^login',views.user_login,name='user_login'),
    url(r'^logout/$',views.user_logout,name='user_logout'),
    url(r'^register/$',views.user_register,name='user_register'),
    url(r'^user_manage/$',views.user_manage,name='user_manage'),
    url(r'^perm_manage/$',views.perm_manage,name='perm_manage'),
    url(r'^user_delete/(?P<user_id>\d+)$',views.user_delete,name='user_delete'),
    url(r'^user_update/(?P<user_id>\d+)$',views.user_update,name='user_update'),
    url(r'^user_add/$',views.user_add,name='user_add'),
    url(r'^group_manage/$',views.group_manage,name='group_manage'),
    url(r'^group_delete/(?P<group_id>\d+)$',views.group_delete,name='group_delete'),
    url(r'^group_update/(?P<group_id>\d+)$',views.group_update,name='group_update'),
    url(r'^group_add/$', views.group_add, name='group_add'),
    url(r'^http_403/$', views.http_403, name='http_403'),
    url(r'^http_404/$', views.http_404, name='http_404'),
    url(r'^remove_user_from_group/(?P<user_id>\d+)/(?P<group_id>\d+)$',views.remove_user_from_group,name='remove_user_from_group'),
    url(r'^add_user_to_group/(?P<user_id>\d+)/(?P<group_id>\d+)',views.add_user_to_group,name='add_user_to_group'),
    url(r'perm_manage/$', views.perm_manage, name='perm_manage'),
    url(r'perm_add/$', views.perm_add, name='perm_add'),
    url(r'perm_delete/(?P<perm_id>\d+)$', views.perm_delete, name='perm_delete'),
    url(r'perm_update/(?P<perm_id>\d+)$', views.perm_update, name='perm_update'),
    url(r'user_perm/(?P<user_id>\d+)$', views.user_perm, name='user_perm'),
    url(r'user_remove_perm/(?P<user_id>\d+)/(?P<perm_id>\d+)$', views.user_remove_perm, name='user_remove_perm'),
    url(r'user_add_perm/(?P<user_id>\d+)/(?P<perm_id>\d+)$', views.user_add_perm, name='user_add_perm'),
    url(r'group_perm/(?P<group_id>\d+)$', views.group_perm, name='group_perm'),
    url(r'group_remove_perm/(?P<group_id>\d+)/(?P<perm_id>\d+)$', views.group_remove_perm, name='group_remove_perm'),
    url(r'group_add_perm/(?P<group_id>\d+)/(?P<perm_id>\d+)$', views.group_add_perm, name='group_add_perm'),
    url(r'activate/(?P<token>\w+.[-_\w]*\w+.[-_\w]*\w+)/$', views.active_user, name='active_user'),
]