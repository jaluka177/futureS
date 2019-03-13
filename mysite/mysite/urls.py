"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from . import views
from django.urls import path
from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home/', views.home),
    url(r'^login/', views.login),
    url(r'^signin/', views.register),
    url(r'^forgot/', views.getpassword),
    url(r'^get_news/', views.get_news),
    url(r'^mo_pass/', views.modifypassword),
    url(r'^modify/', views.modify),
    url(r'^outcome/', views.outcome_news),
    url(r'^smallschool/', views.home),
    url(r'^news_con/', views.news_con),
    url(r'^index/', views.index),


    # url(r'^news/', views.news),

    # url(r'^login1/', auth_views.LoginView.as_view(template_name='login1.html'),name='login1'),
    # url(r'^logout/', auth_views.LogoutView.as_view(template_name='logout.html'),name='logout'),




]
urlpatterns += staticfiles_urlpatterns()