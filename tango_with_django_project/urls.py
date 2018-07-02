"""tango_with_django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from rango import views
from registration.backends.simple.views import RegistrationView
from django.conf.urls.static import static


from blog import upload
from django.views.static import serve
from . import settings

class MyRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return '/rango/'


urlpatterns = [
    url(r'^$', views.index, name='index'),
#    url(r'^admin/uploads/(?P<dir_name>[^/]+)$', upload.upload_image, name='upload_image'),
#    url(r'^upload/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, }),
    url(r'accounts/register/$', MyRegistrationView.as_view(),
        name='registration_register'),
    url(r'^rango/', include('rango.urls')),
    url(r'^blog/', include('blog.urls',namespace='blog')),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^emoji/', include('emoji.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
