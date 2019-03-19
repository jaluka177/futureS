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
    url(r'^recent/', views.recent),
    url(r'^login/', views.login),
    url(r'^signin/', views.register),
    url(r'^forgot/', views.getpassword),
    url(r'^get_news/', views.get_news),
    url(r'^mo_pass/', views.modifypassword),
    url(r'^modify/', views.modify),
    # url(r'^outcome/', views.outcome_news),
    url(r'^smallschool/', views.home1),
    url(r'^news_con/', views.news_con),
    url(r'^index/', views.index),
    url(r'^search/', views.search_news),
    url(r'^income_statement/', views.income_statement),
    url(r'^search_for_keyword/', views.search_news_for_keyword),
    url(r'^list/', views.list_page1),
    url(r'^choice/', views.stock_choice),
    url(r'^stock/', views.stock),
    url(r'^stock_ana/', views.stock_analysis),
    url(r'^cash_flow_statement/', views.cash_flow_statement),
    url(r'^economic_term/', views.economic_term),
    url(r'^tech/', views.tech),
    url(r'^algotrade/', views.algotrade),
    url(r'^new_info/', views.new_info),
url(r'^new_infocon2/', views.new_infocon2),
url(r'^new_infocon3/', views.new_infocon3),
url(r'^new_infocon4/', views.new_infocon4),
url(r'^new_infocon5/', views.new_infocon5),
url(r'^new_infocon/', views.new_infocon),
    # url(r'^predict/', views.predict1),

    url(r'^search_discussion/', views.search_discussion),
    url(r'^chat_outcome/', views.content),
    url(r'^get_article/', views.get_article),
    # url(r'^post_page_1/', views.post_page_1),
    # url(r'^post_page_2/', views.post_page_2),
    # url(r'^post_page_3/', views.post_page_3),
    # url(r'^post_next/', views.post_next),
    # url(r'^post_prev/', views.post_prev),
    # url(r'^reply/', views.reply),
    # url(r'^like/', views.like),
    # url(r'^post/', views.issued),


    # url(r'^news/', views.news),

    # url(r'^login1/', auth_views.LoginView.as_view(template_name='login1.html'),name='login1'),
    # url(r'^logout/', auth_views.LogoutView.as_view(template_name='logout.html'),name='logout'),




]
urlpatterns += staticfiles_urlpatterns()
