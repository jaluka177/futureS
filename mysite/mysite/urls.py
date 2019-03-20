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

    # 登入
    url(r'^login/', views.login),
    url(r'^signin/', views.register),
    url(r'^forgot/', views.getpassword),

    # 首頁
    url(r'^smallschool/', views.home1),

    # 新聞
    # --新聞首頁
    url(r'^get_news/', views.get_news),
    # --新聞文章回傳
    url(r'^outcome/', views.outcome_news),
    # --新聞回傳空白沒資料
    url(r'^news_con/', views.news_con),
    # --新聞查詢小bar
    url(r'^search/', views.search_news),
    url(r'^search_for_keyword/', views.search_news_for_keyword),
    # --新聞查詢 有查日期功能
    url(r'^list/', views.list_page1),

    # 交易資訊
    # --歷史回測
    url(r'^algotrade/', views.algotrade),
    # --期貨專區
    url(r'^stock/', views.stock),
    # 即時資料
    url(r'^recent/', views.recent),
    # --能跑出資料庫資料
    url(r'^index/', views.index),

    # EDITOR

    # 智能機器人
    url(r'^stock_analysis/', views.stock_analysis),

    # --預知未來型
    url(r'^predict/', views.predict),
    # --健康診斷型
    url(r'^stock_ana/', views.stock_analysis),
    # --推薦好股型（開不出來
    url(r'^gep/', views.gep),
    # --買賣型
    url(r'^five/', views.five),
    # --投資組合推薦 (開不出來
    # url(r'^funds/', views.fund_2),

    # 指標專區
    url(r'^economic_term/', views.economic_term),

    # 下單機
    url(r'^tech/', views.tech),

    # 新手專區
    # --討論區
    url(r'^get_article/', views.get_article),
    # --回傳內容
    url(r'^chat_outcome/', views.content),
    url(r'^post_page_1/', views.post_page_1),
    url(r'^post_page_2/', views.post_page_2),
    url(r'^post_page_3/', views.post_page_3),
    url(r'^post_next/', views.post_next),
    url(r'^post_prev/', views.post_prev),
    # url(r'^reply/', views.reply),
    url(r'^like/', views.like),
    # -- 發文（簡單回傳
    url(r'^post/', views.issued),
    # --討論區搜尋(簡單回傳
    url(r'^chat_search/', views.chat_search),

    # 會員
    # --會員首頁
    url(r'^member/', views.member),
    url(r'^mem_home/', views.mem_home),
    # --忘記密碼
    url(r'^mo_pass/', views.modifypassword),
    # --修改基本資料
    url(r'^modify/', views.modify),

    # url(r'^member_news', views.member_news),
    # url(r'^mem_sto/', member_list_add),

    # 開得出來功能但還不知道可以用在哪

    # 損益表
    url(r'^income_statement/', views.income_statement),
    # 現金流量表
    url(r'^cash_flow_statement/', views.cash_flow_statement),
    # 股票代碼查詢
    url(r'^choice/', views.stock_choice),

    # 簡單回傳開不了區

    # url(r'^ inc_sta/', views.inc_sta),
    # url(r'^message/', views.message),
    # url(r'^search_discussion/', views.search_discussion),
    
    ##機器人投顧
    url(r'^funds/', views.fund_2),
    url(r'^portfolio/', views.portfolio),
    url(r'^fundamental/', views.fundamental_information),
    url(r'^analysis1/', views.analysis1),
    url(r'^analysis2/', views.analysis2),
    url(r'^add/', views.add),
    url(r'^gep/', views.gep),
    url(r'^add3/', views.add3),
    url(r'^test', views.fq),
    url(r'^five/', views.five_stock),
    url(r'^add3/', views.add3),


]
urlpatterns += staticfiles_urlpatterns()
