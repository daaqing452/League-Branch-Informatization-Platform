"""LBInformatization URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
import LBInformatization.settings as settings
from SUser.views import index, department, branch, profile, add_user, delete_user
from Message.views import message, uploadFile
from Handbook.views import handbook

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', index),
    url(r'^index/$', index),
    url(r'^department/([0-9]{1,9})/$', department),
    url(r'^branch/([0-9]{1,9})/$', branch),
    url(r'^profile/([0-9]{1,9})/$', profile),
    url(r'^au/([a-z0-9]{1,20})/$', add_user),
    url(r'^du/([a-z0-9]{1,20})/$', delete_user),

    url(r'^message/$', message),
    url(r'^message/([0-9]{1,9})/$', message),
    url(r'^uploadFile/$', uploadFile),
    url(r'^handbook/([b,d])/([0-9]{1,9})$', handbook),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
