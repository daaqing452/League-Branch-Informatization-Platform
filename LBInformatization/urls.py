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
from SUser.views import *
from Message.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', index),
    url(r'^index/$', index),
    url(r'^department/([0-9]{1,9})/$', department),
    url(r'^branch/([0-9]{1,9})/$', branch),
    url(r'^profile/([0-9]{1,9})/$', profile),
    url(r'^au/([a-z0-9]{1,20})/$', add_user),
    url(r'^du/([a-z0-9]{1,20})/$', delete_user),

    url(r'^uploadFile/$', uploadFile),

    url(r'^message/$', message),
    url(r'^message/([0-9]{1,9})/$', message),
    url(r'^handbook/([b,d])/([0-9]{1,9})/$', handbook_edit),
    url(r'^handbook/([0-9]{1,9})/$', handbook_show),
    
    url(r'^news/([0-9]{1,9})/$', news),
    url(r'^news_list/([i])/$', news_list),
    url(r'^news_list/([b,d])/([0-9]{1,9})/$', news_list),
    url(r'^slide_list/([i])/$', slide_list),
    url(r'^slide_list/([b,d])/([0-9]{1,9})/$', slide_list),

    url(r'^jiatuan/b/([0-9]{1,9})/$', jiatuan_edit),
    url(r'^jiatuan/([0-9]{1,9})/$', jiatuan_show),

    url(r'^global_setting/$', global_setting),
    url(r'^amt_setting/(i)/$', amt_setting),
    url(r'^amt_setting/(d)/([0-9]{1,9})/$', amt_setting),

    url(r'^authority_files/$', authority_files),
    url(r'^authority_files_tip/(\d{1,10})/$', authority_files_tip),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
