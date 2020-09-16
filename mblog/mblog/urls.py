"""mblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from mainsite import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from mblog.settings import MEDIA_ROOT
from rest_framework.routers import DefaultRouter
from rest_framework.decorators import list_route
from pages import page_views, file_views




router = DefaultRouter()
router.register(r'dashboard', views.ProfileViewSet)
router.register(r'file',file_views.FileUploadViewSet)
router.register(r'batch',views.BatchViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',page_views.index,name="home"),
    path('login/',page_views.login),
    path('logout/',page_views.logout),
    path('upload/',page_views.simple_upload,name='simple_upload'),
    path('chart/', page_views.chart),
    path('analyse/',page_views.analyse),
    path('userinfo/',page_views.userinfo),
    path('index/',page_views.index),
    # path('media/(?P<path>.*)', serve, {"document_root":MEDIA_ROOT}),
    path('app/',views.save_data),
    path('dashboard/',views.query), # save dashboard info
    path('api/',include(router.urls)),# for get api/dashboard/
    path('xmlupload/',page_views.xml_upload,name='xml_upload'),
    path('numsimulation/',page_views.num_simulation,name='num_simulation'),
    path('deeplearning/',page_views.deep_learning,name='deep_learning'),
    path('alias/', page_views.alias, name='alias'),
    path('opc/', page_views.opc, name='opc'),
    path('usecase/', page_views.usecase, name='usecase'),
    path('batch/', page_views.batch, name='batch'),
    path('preview/', page_views.preview, name='preview'),
    path('exe/', page_views.exe, name='exe'),
    path('register/',page_views.register),
    path('elearning/', page_views.elearning, name='elearning'),
    path('get_table_permission/',file_views.GETTABLEPERMISSION.as_view())
    

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)