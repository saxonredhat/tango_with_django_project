from django.conf.urls import url
from blog import views, upload
from django.views.static import serve
from tango_with_django_project import settings

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^articles_list/$', views.articles_list, name='articles_list'),
    url(r'^article_detail/(?P<article_id>\d+)$', views.article_detail, name='article_detail'),
    url(r'^article_add/$', views.article_add, name='article_add'),
    url(r'^article_update_list/$', views.article_update_list, name='article_update_list'),
    url(r'^article_update/(?P<article_id>\d+)$', views.article_update, name='article_update'),
    url(r'^article_delete_list/$', views.article_delete_list, name='article_delete_list'),
    url(r'^article_delete/(?P<article_id>\d+)$', views.article_delete, name='article_delete'),
    url(r'^article_add_comment/(?P<article_id>\d+)$', views.article_add_comment, name='article_add_comment'),
    url(r'^article_custom_categories_list/',views.article_custom_categories_list,name='article_custom_categories_list'),
    url(r'^article_custom_categories_add/',views.article_custom_categories_add,name='article_custom_categories_add'),
    url(r'^article_custom_categories_delete/(?P<category_name>\w+)$',views.article_custom_categories_delete,name='article_custom_categories_delete'),
    url(r'^comment_user/(?P<comment_id>\d+)/(?P<user_id>\d+)$', views.comment_user, name='comment_user'),
    url(r'^comment_user_first/(?P<comment_id>\d+)/(?P<article_id>\d+)$', views.comment_user_first, name='comment_user_first'),
    url(r'^comment_user_second/(?P<comment_id>\d+)/(?P<article_id>\d+)$', views.comment_user_second, name='comment_user_second'),
    url(r'^comment_delete/(?P<comment_id>\d+)$', views.comment_delete, name='comment_delete'),
    url(r'^comment_list/(?P<article_id>\d+)$', views.comment_list, name='comment_list'),
    url(r'^like_article/(?P<article_id>\d+)$',views.like_article, name='like_article'),
    url(r'^like_user/(?P<user_id>\d+)$',views.like_user, name='like_user'),
    url(r'^like_comment/(?P<comment_id>\d+)$',views.like_comment, name='like_comment'),
    url(r'^login/$', views.user_login, name='user_login'),
    url(r'^logout/$', views.user_logout, name='user_logout'),
    url(r'^register/$', views.user_register, name='user_register'),
    url(r'^user_manage/$', views.user_manage, name='user_manage'),
    url(r'^perm_manage/$', views.perm_manage, name='perm_manage'),
    url(r'^user_delete/(?P<user_id>\d+)$', views.user_delete, name='user_delete'),
    url(r'^user_update/(?P<user_id>\d+)$', views.user_update, name='user_update'),
    url(r'^user_add/$', views.user_add, name='user_add'),
    url(r'^user_info/$', views.user_info, name='user_info'),
    url(r'^user_zone/(?P<user_id>\d+)$', views.user_zone, name='user_zone'),
    url(r'^user_follow/(?P<user_id>\d+)$',views.user_follow,name='user_follow'),
    url(r'^user_followers/(?P<user_id>\d+)$',views.user_followers,name='user_followers'),
    url(r'^user_followees/(?P<user_id>\d+)$', views.user_followees, name='user_followees'),
    url(r'^user_favorite/(?P<article_id>\d+)$', views.user_favorite, name='user_favorite'),
    url(r'^user_favorites/(?P<user_id>\d+)$', views.user_favorites, name='user_favorites'),
    url(r'^user_articles/(?P<user_id>\d+)$', views.user_articles, name='user_articles'),
    url(r'^user_notifications/messages/list/$',views.user_messages_list,name='user_messages_list'),
    url(r'^user_notifications/messages/user/(?P<user_id>\d+)$', views.user_message, name='user_message'),
    url(r'^user_notifications/$', views.user_notifications, name='user_notifications'),
    url(r'^user_search/$', views.user_search, name='user_search'),
    url(r'^user_message/(?P<user_id>\d+)$',views.user_message,name='user_message'),
    url(r'^user_send_message/user/(?P<recevie_user_id>\d+)$', views.user_send_message, name='user_send_message'),
    url(r'^user_get_message/user/(?P<user_id>\d+)',views.user_get_message, name='user_get_message'),
    url(r'^user_un_follower/(?P<user_id>\d+)$', views.user_un_follower, name='user_un_follower'),
    url(r'^user_active/(?P<user_id>\d+)$', views.user_active, name='user_active'),
    url(r'^user_forget_password/$', views.user_forget_password,name='user_forget_password'),
    url(r'^user_change_password/$', views.user_change_password,name='user_change_password'),
    url(r'^user_send_old_email/$', views.user_send_old_email,name='user_send_old_email'),
    url(r'^user_send_new_email/$', views.user_send_new_email, name='user_send_new_email'),
    url(r'^user_verify_old_email/(?P<token>\w+.[-_\w]*\w+.[-_\w]*\w+)/$', views.user_verify_old_email,name='user_verify_old_email'),
    url(r'^user_verify_new_email/(?P<token>\w+.[-_\w]*\w+.[-_\w]*\w+)/$', views.user_verify_new_email,name='user_verify_new_email'),
    url(r'^user_reset_password/(?P<token>\w+.[-_\w]*\w+.[-_\w]*\w+)/$', views.user_reset_password,name='user_reset_password'),
    url(r'^group_manage/$', views.group_manage,name='group_manage'),
    url(r'^group_delete/(?P<group_id>\d+)$',views.group_delete,name='group_delete'),
    url(r'^group_update/(?P<group_id>\d+)$',views.group_update,name='group_update'),
    url(r'^group_add/$', views.group_add, name='group_add'),
    url(r'^http_403/$', views.http_403, name='http_403'),
    url(r'^http_404/$', views.http_404, name='http_404'),
    url(r'^remove_user_from_group/(?P<user_id>\d+)/(?P<group_id>\d+)$',views.remove_user_from_group,name='remove_user_from_group'),
    url(r'^add_user_to_group/(?P<user_id>\d+)/(?P<group_id>\d+)$',views.add_user_to_group,name='add_user_to_group'),
    url(r'^perm_manage/$', views.perm_manage, name='perm_manage'),
    url(r'^perm_add/$', views.perm_add, name='perm_add'),
    url(r'^perm_delete/(?P<perm_id>\d+)$', views.perm_delete, name='perm_delete'),
    url(r'^perm_update/(?P<perm_id>\d+)$', views.perm_update, name='perm_update'),
    url(r'^user_perm/(?P<user_id>\d+)$', views.user_perm, name='user_perm'),
    url(r'^user_remove_perm/(?P<user_id>\d+)/(?P<perm_id>\d+)$', views.user_remove_perm, name='user_remove_perm'),
    url(r'^user_add_perm/(?P<user_id>\d+)/(?P<perm_id>\d+)$', views.user_add_perm, name='user_add_perm'),
    url(r'^group_perm/(?P<group_id>\d+)$', views.group_perm, name='group_perm'),
    url(r'^group_remove_perm/(?P<group_id>\d+)/(?P<perm_id>\d+)$', views.group_remove_perm, name='group_remove_perm'),
    url(r'^group_add_perm/(?P<group_id>\d+)/(?P<perm_id>\d+)$', views.group_add_perm, name='group_add_perm'),
    url(r'^activate/(?P<token>\w+.[-_\w]*\w+.[-_\w]*\w+)/$', views.active_user, name='active_user'),
    url(r'^canvas/$', views.canvas, name='canvas'),
    url(r'^testajax/$', views.testajax, name='testajax'),
    url(r'^testdiv/$', views.testdiv, name='testdiv'),
    #url(r'publish_article'),
    #url(r''),
    #url(r''),
]