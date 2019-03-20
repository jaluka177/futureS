from django.shortcuts import render,render_to_response,HttpResponseRedirect,redirect

from .models import RobotMember, RobotYahooNew, RobotCna, RobotYahooHot, RobotYahooStock, RobotYahooTec, RobotYahooTra, \
    RobotYahoo, RobotYahooTendency, RobotDiscuss, RobotInformation, RobotTransactionInfo, RobotCorporate, \
    RobotTrackStock, RobotCategory, RobotIncomeStatementQ, RobotYahooTendency, RobotCategoryA, RobotCategoryB, \
    RobotListedShares, RobotOverTheCounterShares, RobotMonthrevenue, RobotNews2330, \
    RobotDividendPolicy, RobotMargin, RobotRatio4Q, RobotPe, RobotRatio2Q, RobotRatio2, RobotCashFlowsQ, RobotComment, \
    RobotEconomic, RobotTechnologyIndex, RobotFqType, Discuss, Comment
from django.contrib.auth import authenticate, login
from . import views
from django.views.generic import View
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.mail import send_mail
import random,datetime
# from .k_diagram import predict_eps_season, predict_eps_year

from datetime import date
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# 登入

def login(request):  # 登入功能
    status_m = False
    status_p = False
    back = request.GET.get('back', 0)
    article_id = request.GET.get('article_id', 0)
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        check_m = RobotMember.objects.filter(email__exact=username)
        check_p = RobotMember.objects.filter(password__exact=password)

        if check_m is not None:
            status_m = True
        if check_p is not None:
            status_p = True

        user = RobotMember.objects.filter(email=username, password=password)

        if user and status_m is True and status_p is True:
            request.session['userName'] = user[0].email
            request.session['password'] = user[0].password
            request.session['name'] = user[0].member_name
            if back == '0' or back == '':
                return HttpResponseRedirect('/recent/')
        #     elif back == '討論區發文':
        #         return HttpResponseRedirect('/post/')
        #     elif back == '討論區回覆':
        #         return HttpResponseRedirect('/chat_outcome/?id='+article_id)
        #     elif back == '未來型預測':
        #         return HttpResponseRedirect('/predict/')
        #     elif back == '修改基本資料':
        #         return HttpResponseRedirect('/modify/')
        #     elif back == '修改密碼':
        #         return HttpResponseRedirect('/mo_pass/')
        #     elif back == '新聞首頁':
        #         return HttpResponseRedirect('/get_news/')
        #     elif back == '系統首頁':
        #         return HttpResponseRedirect('/recent/')
        #     elif back == 'My_News':
        #         return HttpResponseRedirect('/member_news/')
        else:
            return render_to_response('login.html', {'status_m': status_m, 'status_p': status_p})

    return render_to_response('login.html', {'back': back, 'article_id': article_id})


def register(request):
    status_m = True
    status_p = True
    status_check_password = True

    if request.method == 'POST':
        check_mail = request.POST.get('mail', '')
        check_password = request.POST.get('password', '')

        check_m = RobotMember.objects.filter(email__exact=check_mail)
        check_p = RobotMember.objects.filter(password__exact=check_password)

        if check_m:  #如果回傳陣列是空的
            status_m = False
        if check_p:  #如果回傳陣列是空的
            status_p = False

        p1 = request.POST.get('password', '')
        p2 = request.POST.get('password_check', '')

        if p1 == p2:  #!=改成is not
            status_check_password = True
        else:
            status_check_password = False

        name = request.POST.get('name', '')
        email = request.POST.get('mail', '')
        password = request.POST.get('password', '')
        phone = request.POST.get('tel', '')

        if status_m is True and status_p is True and status_check_password is True:

            RobotMember.objects.create(member_name=name, email=email, password=password, phone_num=phone, type='1')
            return HttpResponseRedirect('/index/')
        else:
            return render_to_response('signin.html', {'status_m': status_m, 'status_p': status_p,
                                                      'status_check-password': status_check_password, 'name': name,
                                                      'mail': email, 'password': password, 'tel': phone})

    return render_to_response('signin.html', {'status_m': status_m, 'status_p': status_p,
                                              'status_check_password': status_check_password})


def getpassword(request):
    if request.method == 'POST':
        mail = request.POST.get('mail', '')
        check_mail = RobotMember.objects.filter(email=mail)

        if check_mail is not None:
            new_password = random.randint(10000, 100000)
            new_password = str(new_password)
            send_mail('Your New Password', new_password, 'kfjet123@gmail.com', [mail, ], fail_silently=False)
            check_mail.update(password=new_password)
            return render_to_response('login.html')
        else:
            status_m = False
            return render_to_response('forgot.html', {'warn': status_m})

    return render_to_response('forgot.html')


# 首頁

def home1(request):  # 理財小學堂
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    return render_to_response('smallschool.html', {'name': name, 'loginstatus': loginstatus})

# 新聞
def get_news(request):  #check
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    #新聞首頁關於最新頭條 國際財經 熱門點閱 台股盤勢 個股動態 科技產業 傳統產業的顯示文章數
    result = []
    result_2 = []
    result_3 = []
    result_4 = []
    result_5 = []
    result_6 = []
    result_7 = []
    last = RobotYahooNew.objects.order_by('-date')
    last2 = RobotCna.objects.order_by('-date')
    last3 = RobotYahooHot.objects.order_by('-date')
    last4 = RobotYahoo.objects.order_by('-date')
    last5 = RobotYahooStock.objects.order_by('-date')
    last6 = RobotYahooTec.objects.order_by('-date')
    last7 = RobotYahooTra.objects.order_by('-date')

    for n in range(0, 7):
        result.append(last[n])

    for n in range(0, 7):
        result_2.append(last2[n])

    for n in range(0, 7):
        result_3.append(last3[n])

    for n in range(0, 6):
        result_4.append(last4[n])

    for n in range(0, 6):
        result_5.append(last5[n])

    for n in range(0, 6):
        result_6.append(last6[n])

    for n in range(0, 6):
        result_7.append(last7[n])

    return render_to_response('news.html',
                              {'breaking_news': result, 'global': result_2, 'hot': result_3, 't_all': result_4,
                               'stock': result_5, 'tec': result_6, 'tra': result_7, 'name': name,
                               'loginstatus': loginstatus})


# --新聞文章回傳
def outcome_news(request):  #搜尋文章結果 check
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    type = request.GET.get('id', 0)
    status_next = True
    status_prev = True
    if type is '1':
        category = '最新頭條'
        result = request.GET.get('c', 0)
        res = RobotYahooNew.objects.filter(title=result)[0]
        last = RobotYahooNew.objects.last().id
        if res.id is 1:
            status_prev = False
            next_article = RobotYahooNew.objects.get(id=res.id + 1)
            return render_to_response('news_con.html', {'status_prev': status_prev, 'status_next': status_next,
                                                        'next_article': next_article, 'category': category, 'id': type,
                                                        'result': res, 'name': name, 'loginstatus': loginstatus})
        elif res.id is last:
            status_next = False
            prev_article = RobotYahooNew.objects.get(id=res.id - 1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,
                                                        'prev_article': prev_article, 'category': category, 'id': type,
                                                        'result': res, 'name': name, 'loginstatus': loginstatus})
        else:
            next_article = RobotYahooNew.objects.get(id=res.id + 1)
            prev_article = RobotYahooNew.objects.get(id=res.id - 1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,
                                                        'prev_article': prev_article, 'next_article': next_article,
                                                        'category': category, 'id': type, 'result': res, 'name': name,
                                                        'loginstatus': loginstatus})

    if type is '2':
        category = '國際財經'
        result = request.GET.get('c', 0)
        res = RobotCna.objects.filter(title=result)[0]
        last = RobotCna.objects.last().id
        if res.id is 520:
            status_prev = False
            next_article = RobotCna.objects.get(id=res.id + 1)
            return render_to_response('news_con.html', {'status_prev': status_prev, 'status_next': status_next,
                                                        'next_article': next_article, 'category': category, 'id': type,
                                                        'result': res, 'name': name, 'loginstatus': loginstatus})
        elif res.id is last:
            status_next = False
            prev_article = RobotCna.objects.get(id=res.id - 1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,
                                                        'prev_article': prev_article, 'category': category, 'id': type,
                                                        'result': res, 'name': name, 'loginstatus': loginstatus})
        else:
            next_article = RobotCna.objects.get(id=res.id + 1)
            prev_article = RobotCna.objects.get(id=res.id - 1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,
                                                        'prev_article': prev_article, 'next_article': next_article,
                                                        'category': category, 'id': type, 'result': res, 'name': name,
                                                        'loginstatus': loginstatus})

    if type is '3':
        category = '熱門點閱'
        result = request.GET.get('c', 0)
        res = RobotYahooHot.objects.filter(title=result)[0]
        last = RobotYahooHot.objects.last().id
        if res.id is 1:
            status_prev = False
            next_article = RobotYahooHot.objects.get(id=res.id + 1)
            return render_to_response('news_con.html', {'status_prev': status_prev, 'status_next': status_next,
                                                        'next_article': next_article, 'category': category, 'id': type,
                                                        'result': res, 'name': name, 'loginstatus': loginstatus})
        elif res.id is last:
            status_next = False
            prev_article = RobotYahooHot.objects.get(id=res.id - 1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,
                                                        'prev_article': prev_article, 'category': category, 'id': type,
                                                        'result': res, 'name': name, 'loginstatus': loginstatus})
        else:
            next_article = RobotYahooHot.objects.get(id=res.id + 1)
            prev_article = RobotYahooHot.objects.get(id=res.id - 1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,
                                                        'prev_article': prev_article, 'next_article': next_article,
                                                        'category': category, 'id': type, 'result': res, 'name': name,
                                                        'loginstatus': loginstatus})

    if type is '4':
        category = '台股盤勢'
        result = request.GET.get('c', 0)
        res = RobotYahoo.objects.filter(title=result)[0]
        last = RobotYahoo.objects.last().id
        if res.id is 1:
            status_prev = False
            next_article = RobotYahoo.objects.get(id=res.id + 1)
            return render_to_response('news_con.html', {'status_prev': status_prev, 'status_next': status_next,
                                                        'next_article': next_article, 'category': category, 'id': type,
                                                        'result': res, 'name': name, 'loginstatus': loginstatus})
        elif res.id is last:
            status_next = False
            prev_article = RobotYahoo.objects.get(id=res.id - 1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,
                                                        'prev_article': prev_article, 'category': category, 'id': type,
                                                        'result': res, 'name': name, 'loginstatus': loginstatus})
        else:
            next_article = RobotYahoo.objects.get(id=res.id + 1)
            prev_article = RobotYahoo.objects.get(id=res.id - 1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,
                                                        'prev_article': prev_article, 'next_article': next_article,
                                                        'category': category, 'id': type, 'result': res, 'name': name,
                                                        'loginstatus': loginstatus})

    if type is '5':
        category = '個股動態'
        result = request.GET.get('c', 0)
        res = RobotYahooStock.objects.filter(title=result)[0]
        last = RobotYahooStock.objects.last().id
        if res.id is 1:
            status_prev = False
            next_article = RobotYahooStock.objects.get(id=res.id + 1)
            return render_to_response('news_con.html', {'status_prev': status_prev, 'status_next': status_next,
                                                        'next_article': next_article, 'category': category, 'id': type,
                                                        'result': res, 'name': name, 'loginstatus': loginstatus})
        elif res.id is last:
            status_next = False
            prev_article = RobotYahooStock.objects.get(id=res.id - 1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,
                                                        'prev_article': prev_article, 'category': category, 'id': type,
                                                        'result': res, 'name': name, 'loginstatus': loginstatus})
        else:
            next_article = RobotYahooStock.objects.get(id=res.id + 1)
            prev_article = RobotYahooStock.objects.get(id=res.id - 1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,
                                                        'prev_article': prev_article, 'next_article': next_article,
                                                        'category': category, 'id': type, 'result': res, 'name': name,
                                                        'loginstatus': loginstatus})

    if type is '6':
        category = '科技產業'
        result = request.GET.get('c', 0)
        res = RobotYahooTec.objects.filter(title=result)[0]
        last = RobotYahooTec.objects.last().id
        if res.id is 1:
            status_prev = False
            next_article = RobotYahooTec.objects.get(id=res.id + 1)
            return render_to_response('news_con.html', {'status_prev': status_prev, 'status_next': status_next,
                                                        'next_article': next_article, 'category': category, 'id': type,
                                                        'result': res, 'name': name, 'loginstatus': loginstatus})
        elif res.id is last:
            status_next = False
            prev_article = RobotYahooTec.objects.get(id=res.id - 1)
            return render_to_response('news_con.html', {'status_next': status_next, 'satus_prev': status_prev,
                                                        'prev_article': prev_article, 'category': category, 'id': type,
                                                        'result': res, 'name': name, 'loginstatus': loginstatus})
        else:
            next_article = RobotYahooTec.objects.get(id=res.id + 1)
            prev_article = RobotYahooTec.objects.get(id=res.id - 1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,
                                                        'prev_article': prev_article, 'next_article': next_article,
                                                        'category': category, 'id': type, 'result': res, 'name': name,
                                                        'loginstatus': loginstatus})

    if type is '7':
        category = '傳統產業'
        result = request.GET.get('c', 0)
        res = RobotYahooTra.objects.filter(title=result)[0]
        last = RobotYahooTra.objects.last().id
        if res.id is 1:
            status_prev = False
            next_article = RobotYahooTra.objects.get(id=res.id + 1)
            return render_to_response('news_con.html', {'status_prev': status_prev, 'status_next': status_next,
                                                        'next_article': next_article, 'category': category, 'id': type,
                                                        'result': res, 'name': name, 'loginstatus': loginstatus})
        elif res.id is last:
            status_next = False
            prev_article = RobotYahooTra.objects.get(id=res.id - 1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,
                                                        'prev_article': prev_article, 'category': category, 'id': type,
                                                        'result': res, 'name': name, 'loginstatus': loginstatus})
        else:
            next_article = RobotYahooTra.objects.get(id=res.id + 1)
            prev_article = RobotYahooTra.objects.get(id=res.id - 1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,
                                                        'prev_article': prev_article, 'next_article': next_article,
                                                        'category': category, 'id': type, 'result': res, 'name': name,
                                                        'loginstatus': loginstatus})

    if type is '8':
        category = '國際財經'
        result = request.GET.get('c', 0)
        res = RobotCna.objects.objects.filter(title=result)[0]
        last = RobotCna.objects.last().id
        if res.id is 1:
            status_prev = False
            next_article = RobotCna.objects.get(id=res.id + 1)
            return render_to_response('news_con.html', {'status_prev': status_prev, 'status_next': status_next,
                                                        'next_article': next_article, 'category': category, 'id': type,
                                                        'result': res, 'name': name, 'loginstatus': loginstatus})
        elif res.id is last:
            status_next = False
            prev_article = RobotCna.objects.get(id=res.id - 1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,
                                                        'prev_article': prev_article, 'category': category, 'id': type,
                                                        'result': res, 'name': name, 'loginstatus': loginstatus})
        else:
            next_article = RobotCna.objects.get(id=res.id + 1)
            prev_article = RobotCna.objects.get(id=res.id - 1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,
                                                        'prev_article': prev_article, 'next_article': next_article,
                                                        'category': category, 'id': type, 'result': res, 'name': name,
                                                        'loginstatus': loginstatus})

    if type is '9':
        category = '熱門關鍵字'
        result = request.GET.get('c', 0)
        res = RobotYahooTendency.objects.filter(title=result)[0]
        last = RobotYahooTendency.objects.last().id
        if res.id is 1:
            status_prev = False
            next_article = RobotYahooTendency.objects.get(id=res.id + 1)
            return render_to_response('news_con.html', {'status_prev': status_prev, 'status_next': status_next,
                                                        'next_article': next_article, 'category': category, 'id': type,
                                                        'result': res, 'name': name, 'loginstatus': loginstatus})
        elif res.id is last:  # 目前只有12筆 之後會增加到30多筆
            status_next = False
            prev_article = RobotYahooTendency.objects.get(id=res.id - 1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,
                                                        'prev_article': prev_article, 'category': category, 'id': type,
                                                        'result': res, 'name': name, 'loginstatus': loginstatus})
        else:
            next_article = RobotYahooTendency.objects.get(id=res.id + 1)
            prev_article = RobotYahooTendency.objects.get(id=res.id - 1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,
                                                        'prev_article': prev_article, 'next_article': next_article,
                                                        'category': category, 'id': type, 'result': res, 'name': name,
                                                        'loginstatus': loginstatus})


# --新聞回傳空白沒資料
def news_con(request):

    return render(request, 'news_con.html')


# --新聞查詢小bar
def search_news(request):  # 查詢文章關鍵字 check
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    search_status = False  # 尚未查詢文章前狀態為false
    res_1 = []
    res_2 = []
    res_3 = []
    res_4 = []
    res_5 = []
    res_6 = []
    res_7 = []
    res_8 = []
    res_9 = []
    res_10 = []
    res_11 = []
    res_12 = []
    key2 = '關鍵字'
    if request.method == 'POST':
        search_status = True  # 開始查詢後狀態為True
        for_member = request.POST.get('search2', '')
        key = request.POST.get('search', '')
        if for_member != '':
            key = for_member[5:]
        else:
            pass

        yahoo_new_res_1 = RobotYahooNew.objects.filter(title__contains=key, content__contains=key).order_by('-date')
        yahoo_res_1 = RobotYahoo.objects.filter(title__contains=key, content__contains=key).order_by('-date')
        yahoo_stock_res_1 = RobotYahooStock.objects.filter(title__contains=key, content__contains=key).order_by('-date')
        yahoo_stock_res_2 = RobotYahooStock.objects.filter(tag__contains=key, content__contains=key).order_by('-date')
        yahoo_tec_res_1 = RobotYahooTec.objects.filter(title__contains=key, content__contains=key).order_by('-date')
        yahoo_tec_res_2 = RobotYahooTec.objects.filter(content__contains=key).order_by('-date')
        yahoo_tra_res_1 = RobotYahooTra.objects.filter(title__contains=key, content__contains=key).order_by('-date')
        yahoo_tra_res_2 = RobotYahooTra.objects.filter(tag__contains=key, content__contains=key).order_by('-date')
        yahoo_hot_res_1 = RobotYahooHot.objects.filter(title__contains=key, content__contains=key).order_by('-date')
        yahoo_hot_res_2 = RobotYahooHot.objects.filter(tag__contains=key, content__contains=key).order_by('-date')
        cna_res_1 = RobotCna.objects.filter(title__contains=key, content__contains=key).order_by('-date')

        if yahoo_new_res_1:
            res_12 = yahoo_new_res_1
        if yahoo_res_1:
            res_1 = yahoo_res_1
        if yahoo_stock_res_1:
            res_2 = yahoo_stock_res_1
        if yahoo_stock_res_2:
            res_3 = yahoo_stock_res_2
        if yahoo_tec_res_1:
            res_4 = yahoo_tec_res_1
        if yahoo_tec_res_2:
            res_5 = yahoo_tec_res_2
        if yahoo_tra_res_1:
            res_6 = yahoo_tra_res_1
        if yahoo_tra_res_2:
            res_7 = yahoo_tra_res_2
        if yahoo_hot_res_1:
            res_9 = yahoo_hot_res_1
        if yahoo_hot_res_2:
            res_10 = yahoo_hot_res_2
        if cna_res_1:
            res_11 = cna_res_1
        return render_to_response('news_search.html',
                                  {'res_1': res_1, 'res_2': res_2, 'res_3': res_3, 'res_4': res_4, 'res_5': res_5,
                                   'res_6': res_6, 'res_7': res_7, 'res_9': res_9, 'res_10': res_10, 'res_11': res_11,
                                   'res_12': res_12, 'status': search_status, 'key_word': key, 'name': name,
                                   'loginstatus': loginstatus, 'key2': key2})

    return render_to_response('news_search.html',
                              {'res_1': res_1, 'res_2': res_2, 'res_3': res_3, 'res_4': res_4, 'res_5': res_5,
                               'res_6': res_6, 'res_7': res_7, 'res_9': res_9, 'res_10': res_10, 'res_11': res_11,
                               'res_12': res_12, 'status': search_status, 'name': name, 'loginstatus': loginstatus,
                               'key2': key2})  # check# #

def search_news_for_keyword(request):  # check
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    key2 = '關鍵字'
    keyword = request.GET.get('key', 0)
    yahoo_tendency_res_1 = RobotYahooTendency.objects.filter(tag0=keyword).order_by('-date')
    yahoo_tendency_res_2 = RobotYahooTendency.objects.filter(tag1=keyword).order_by('-date')
    identity = request.GET.get('id', 0)
    status = True
    return render_to_response('news_search.html',
                              {'result_1': yahoo_tendency_res_1, 'result_2': yahoo_tendency_res_2, 'id': identity,
                               'key_word': keyword, 'status': status, 'name': name, 'loginstatus': loginstatus,
                               'key2': key2})


# --新聞查詢 有查日期功能
def list_page1(request):  # more: 第一頁 抓出該新聞類別的資料 check
    date = datetime.now().strftime('%Y-%m-%d')
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    category = request.GET.get('category', 0)
    page_2 = request.GET.get('page', '')
    # page_2 = int(page_2)
    type = request.GET.get('id', 0)
    if type is '1':
        news_list = RobotYahooNew.objects.order_by('-date')
        paginator = Paginator(news_list, 30)
        try:
            news = paginator.page(page_2)
        except PageNotAnInteger:
            news = paginator.page(1)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)
        return render_to_response('news_list.html',
                                  {'date': date, 'news_list': news, 'id': type, 'category': category, 'name': name,
                                   'loginstatus': loginstatus})
    elif type is '2':
        news_list = RobotCna.objects.order_by('-date')
        paginator = Paginator(news_list, 30)
        try:
            news = paginator.page(page_2)
        except PageNotAnInteger:
            news = paginator.page(1)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)
        return render_to_response('news_list.html',
                                  {'date': date, 'news_list': news, 'id': type, 'category': category, 'name': name,
                                   'loginstatus': loginstatus})
    elif type is '3':
        news_list = RobotYahooHot.objects.order_by('-date')
        paginator = Paginator(news_list, 30)
        try:
            news = paginator.page(page_2)
        except PageNotAnInteger:
            news = paginator.page(1)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)
        return render_to_response('news_list.html',
                                  {'date': date, 'news_list': news, 'id': type, 'category': category, 'name': name,
                                   'loginstatus': loginstatus})
    elif type is '4':
        news_list = RobotYahoo.objects.order_by('-date')
        paginator = Paginator(news_list, 30)
        try:
            news = paginator.page(page_2)
        except PageNotAnInteger:
            news = paginator.page(1)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)
        return render_to_response('news_list.html',
                                  {'date': date, 'news_list': news, 'id': type, 'category': category, 'name': name,
                                   'loginstatus': loginstatus})
    elif type is '5':
        news_list = RobotYahooStock.objects.order_by('-date')
        paginator = Paginator(news_list, 30)
        try:
            news = paginator.page(page_2)
        except PageNotAnInteger:
            news = paginator.page(1)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)
        return render_to_response('news_list.html',
                                  {'date': date, 'news_list': news, 'id': type, 'category': category, 'name': name,
                                   'loginstatus': loginstatus})
    elif type is '6':
        news_list = RobotYahooTec.objects.order_by('-date')
        paginator = Paginator(news_list, 30)
        try:
            news = paginator.page(page_2)
        except PageNotAnInteger:
            news = paginator.page(1)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)
        return render_to_response('news_list.html',
                                  {'date': date, 'news_list': news, 'id': type, 'category': category, 'name': name,
                                   'loginstatus': loginstatus})
    else:
        news_list = RobotYahooTra.objects.order_by('-date')
        paginator = Paginator(news_list, 30)
        try:
            news = paginator.page(page_2)
        except PageNotAnInteger:
            news = paginator.page(1)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)
        return render_to_response('news_list.html',
                                  {'date': date, 'news_list': news, 'id': type, 'category': category, 'name': name,
                                   'loginstatus': loginstatus})


# 交易資訊
# --歷史回測
def algotrade(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    stock_list = RobotTrackStock.objects.filter(member_id=1)
    stock = []  # 會員已有的股票
    stock_select = []  # 勾選的股票
    stock_final = []  # 勾選的股票(最多三個)
    times_list = []
    money_final_list = []
    money_begin_list = []
    stock_name_list = []
    money_begin = 0
    money_now = 0
    quantity = 0
    times = 0  # 交易次數

    for n1 in range(0, len(stock_list)):
        stock.append(stock_list[n1].stock_id)
    if request.method == 'POST':  # 開始選股
        for x in range(0, len(stock)):
            stock_select.append(request.POST.get(stock[x], '0'))  # 接 選的股票
        for y in range(0, len(stock_select)):
            if stock_select[y] != '0':
                stock_final.append(stock_select[y])
        stock_ff = set(stock_final)  # 去除重複
        stock_final = list(stock_ff)
        print(stock_final)  # 刪
        money_begin = request.POST.get('money', '0')  # 資金100萬
        money_now = int(money_begin) * 10000
        money_list_all = []
        money_list = []
        month_begin = str(request.POST.get('begin_month', '0'))
        month_end = str(request.POST.get('end_month', '0'))
        year_b = month_begin.split('-')[0]  # 2014
        month_b = month_begin.split('-')[1]  # 08
        year_e = month_end.split('-')[0]  # 2015
        month_e = month_end.split('-')[1]  # 12
        quantity_list = []  # 待修改!!
        print(year_b)  # 刪
        print(month_b)  # 刪
        print(year_e)  # 刪
        print(month_e)  # 刪
        for n in range(0, len(stock_final)):  # 進出場條件
            money_begin_list.append(money_now)
            money_list.append(money_now)
            # 進場條件一: 日,周,月 KD黃金交叉 KD值20,50,80以下
            buy_select1 = request.POST.get('buy_check1', '0')  # 選進場條件1
            buy1_1 = request.POST.get('buy1_1', '0')  # day,week,month KD
            buy1_2 = float(request.POST.get('buy1_2', '0'))  # KD值20,50,80以下
            print(buy_select1)  # 刪
            print(buy1_1)  # 刪
            print(buy1_2)  # 刪
            # 出場條件一: 日,周,月 KD死亡交叉 KD值20,50,80以上
            sell_select1 = request.POST.get('sell_check1', '0')  # 選出場條件1
            sell1_1 = request.POST.get('sell1_1', '0')  # day,week,month KD
            sell1_2 = float(request.POST.get('sell1_2', '0'))  # KD值 20,50,80 以上
            print(sell_select1)  # 刪
            print(sell1_1)  # 刪
            print(sell1_2)  # 刪
            k = 0
            d = 0
            day_all_list = []  # 抓全部日期的技術資料
            list_now = []  # 月份暫存
            date_now = ''
            year_b_int = int(year_b)  # 2014
            year_e_int = int(year_e)  # 2015
            month_b_int = int(month_b)  # 8
            month_e_int = int(month_e)  # 11
            year_limit = year_e_int - year_b_int + 1  # 2015-2014+1
            for x1 in range(0, year_limit):  # 2015-2014+1
                if year_b_int < year_e_int:
                    month_limit = 12 - month_b_int + 1  # 12-8+1
                    for x2 in range(0, month_limit):  # 12-8+1
                        if month_b_int <= 9:
                            date_now = str(year_b_int) + '0' + str(month_b_int)  # date_now去抓
                            list_now = RobotTechnologyIndex.objects.filter(stock_id=stock_final[n],
                                                                           date__startswith=date_now).order_by('date')
                            for l in range(0, len(list_now)):
                                day_all_list.append(list_now[l])
                            month_b_int += 1
                        elif month_b_int <= 12:
                            date_now = str(year_b_int) + str(month_b_int)  # date_now去抓
                            list_now = RobotTechnologyIndex.objects.filter(stock_id=stock_final[n],
                                                                           date__startswith=date_now).order_by('date')
                            for l in range(0, len(list_now)):
                                day_all_list.append(list_now[l])
                            month_b_int += 1
                    if month_b_int == 13:
                        year_b_int += 1
                        month_b_int = 1
                elif year_b_int == year_e_int:
                    month_limit = month_e_int - month_b_int + 1  # 11-1+1
                    for x3 in range(0, month_limit):  # 11-1+1
                        if month_b_int <= 9:
                            date_now = str(year_b_int) + '0' + str(month_b_int)  # date_now去抓
                            list_now = RobotTechnologyIndex.objects.filter(stock_id=stock_final[n],
                                                                           date__startswith=date_now).order_by('date')
                            for l in range(0, len(list_now)):
                                day_all_list.append(list_now[l])
                            month_b_int += 1
                        elif month_b_int <= 12:
                            date_now = str(year_b_int) + str(month_b_int)  # date_now去抓
                            list_now = RobotTechnologyIndex.objects.filter(stock_id=stock_final[n],
                                                                           date__startswith=date_now).order_by('date')
                            for l in range(0, len(list_now)):
                                day_all_list.append(list_now[l])
                            month_b_int += 1
            print(day_all_list)
            print(len(day_all_list))
            for y in range(0, len(day_all_list)):
                if buy_select1 == '1':
                    if buy1_1 == 'day':
                        k = float(day_all_list[y].day_K)
                        d = float(day_all_list[y].day_D)
                        if d < k < buy1_2 and d < buy1_2 and money_now > 0:
                            # 買
                            buy_date = day_all_list[y].date
                            close = float(
                                RobotTransactionInfo.objects.get(stock_id=stock_final[n], date=buy_date).the_close)
                            quantity = round((float(money_now) / close), 2)
                            quantity_list.append(quantity)
                            money_now = 0
                            money_list.append(money_now)
                            times += 1
                            print(stock_final[n])
                            print(buy_date)
                            print(quantity)
                            print(times)
                    if buy1_1 == 'week':
                        k = float(day_all_list[y].week_K)
                        d = float(day_all_list[y].week_D)
                        if d < k < buy1_2 and d < buy1_2 and money_now > 0:
                            # 買
                            buy_date = day_all_list[y].date
                            close = float(
                                RobotTransactionInfo.objects.get(stock_id=stock_final[n], date=buy_date).the_close)
                            quantity = round((float(money_now) / close), 2)
                            quantity_list.append(quantity)
                            money_now = 0
                            money_list.append(money_now)
                            times += 1
                            print(stock_final[n])
                            print(buy_date)
                            print(quantity)
                            print(times)
                    if buy1_1 == 'month':
                        k = float(day_all_list[y].month_K)
                        d = float(day_all_list[y].month_D)
                        if d < k < buy1_2 and d < buy1_2 and money_now > 0:
                            # 買
                            buy_date = day_all_list[y].date
                            close = float(
                                RobotTransactionInfo.objects.get(stock_id=stock_final[n], date=buy_date).the_close)
                            quantity = round((float(money_now) / close), 2)
                            quantity_list.append(quantity)
                            money_now = 0
                            money_list.append(money_now)
                            times += 1
                            print(stock_final[n])
                            print(buy_date)
                            print(quantity)
                            print(times)
                if sell_select1 == '1':
                    if sell1_1 == 'day':
                        k = float(day_all_list[y].day_K)
                        d = float(day_all_list[y].day_D)
                        if d > k > sell1_2 and d > sell1_2 and quantity > 0:
                            # 賣
                            sell_date = day_all_list[y].date
                            close = float(
                                RobotTransactionInfo.objects.get(stock_id=stock_final[n], date=sell_date).the_close)
                            money_earn = round((float(quantity) * close), 2)
                            quantity = 0
                            money_now += money_earn
                            money_list.append(money_now)
                            times += 1
                            print(stock_final[n])
                            print(sell_date)
                            print(money_earn)
                            print(money_now)
                            print(times)
                    if sell1_1 == 'week':
                        k = float(day_all_list[y].week_K)
                        d = float(day_all_list[y].week_D)
                        if d > k > sell1_2 and d > sell1_2 and quantity > 0:
                            # 賣
                            sell_date = day_all_list[y].date
                            close = float(
                                RobotTransactionInfo.objects.get(stock_id=stock_final[n], date=sell_date).the_close)
                            money_earn = round((float(quantity) * close), 2)
                            quantity = 0
                            money_now += money_earn
                            money_list.append(money_now)
                            times += 1
                            print(stock_final[n])
                            print(sell_date)
                            print(money_earn)
                            print(money_now)
                            print(times)
                    if sell1_1 == 'month':
                        k = float(day_all_list[y].month_K)
                        d = float(day_all_list[y].month_D)
                        if d > k > sell1_2 and d > sell1_2 and quantity > 0:
                            # 賣
                            sell_date = day_all_list[y].date
                            close = float(
                                RobotTransactionInfo.objects.get(stock_id=stock_final[n], date=sell_date).the_close)
                            money_earn = round((float(quantity) * close), 2)
                            quantity = 0
                            money_now += money_earn
                            money_list.append(money_now)
                            times += 1
                            print(stock_final[n])
                            print(sell_date)
                            print(money_earn)
                            print(money_now)
                            print(times)

            times_list.append(times)
            times = 0  # 此股票交易次數歸零
            money_final_list.append(money_now)  # 期末資金
            money_now = int(money_begin) * 10000  # 還原初始資金
            quantity = 0
            stock_name_list.append(RobotInformation.objects.get(stock_id=stock_final[n]).co_name)
            money_list_all.append(money_list)
            money_list = []

        gross_profit_list = []
        gross_loss_list = []
        gross_list = []
        gain_list = []  # 勝率
        total_1_list = []  # 平均交易金額
        total_3_list = []  # 平均獲利交易金額
        total_4_list = []  # 平均虧損交易金額
        total_5_list = []  # 平均獲利/平均虧損(%)
        total_6_list = []  # 獲利因子  毛利/毛損
        profit_data_final = []  # 最大交易獲利
        loss_data_final = []  # 最大交易虧損
        profit_data_2 = []  # 存1-3個list
        loss_data_2 = []
        profit_data = []
        loss_data = []
        max_profit_final = []  # 單筆最高報酬
        max_loss_final = []  # 單筆最低報酬
        max_profit_list = []  # 存1-3個list(最高報酬 所有數據)
        max_loss_list = []
        max_profit = []  # 最高報酬(相除後) 所有數據
        max_loss = []
        max_profit_2 = []  # 存1-3個list(money)
        max_loss_2 = []
        max_profit_money = []  # money
        max_loss_money = []
        for n in range(0, len(money_list_all)):
            ga = 0
            gb = 0
            gc = 0
            gross_profit = 0  # 毛利
            gross_loss = 0  # 毛損
            gross = 0  # 損益
            count_profit = 0
            count_loss = 0
            gain = 0  # 勝率
            total_1 = 0  # 所有交易金額
            total_2 = 0  # 平均交易金額
            total_3 = 0  # 平均獲利交易金額
            total_4 = 0  # 平均虧損交易金額
            total_5 = 0  # 平均獲利/平均虧損(%)
            data1 = 0  # profit_data = []
            data2 = 0  # loss_data = []
            for x in range(2, len(money_list_all[n])):  # 毛利毛損
                if money_list_all[n][x] != 0:
                    money1 = float(money_list_all[n][x])
                    money2 = float(money_list_all[n][x - 2])
                    if money1 > money2:  # 獲利
                        data1 = round((money1 - money2), 2)
                        profit_data.append(data1)
                        gross_profit += data1
                        count_profit += 1
                        max_profit_money.append(money2)
                    elif money1 < money2:  # 虧損
                        data2 = round((money2 - money1), 2)
                        loss_data.append(data2)
                        gross_loss += data2
                        count_loss += 1
                        max_loss_money.append(money2)
            for y in range(0, len(money_list_all[n])):
                total_1 += money_list_all[n][y]
                if times_list[n] != 0:
                    total_2 = round((total_1 / times_list[n]), 2)
            if count_profit != 0:
                total_3 = round((gross_profit / count_profit), 2)
            if count_loss != 0:
                total_4 = round((gross_loss / count_loss), 2)
            total_3_list.append(total_3)
            total_4_list.append(total_4)
            if total_4 != 0:
                total_5 = round((total_3 / total_4) * 100, 2)
            total_5_list.append(total_5)
            total_1_list.append(total_2)
            gross = round((gross_profit - gross_loss), 2)
            ga = gross_profit
            gb = gross_loss
            gross_profit_list.append(round(gross_profit, 2))
            gross_loss_list.append(round(gross_loss, 2))
            if gb != 0:
                gc = round((ga / gb), 2)  # # 獲利因子  毛利/毛損
            # else:
            #    gc = 0.9
            total_6_list.append(gc)
            gross_list.append(gross)
            if times_list[n] != 0:
                gain = round((count_profit / times_list[n]) * 100, 2)
            gain_list.append(gain)
            # gain_list = [80, 72]
            profit_data_2.append(profit_data)
            loss_data_2.append(loss_data)
            profit_data = []
            loss_data = []
            max_profit_2.append(max_profit_money)
            max_loss_2.append(max_loss_money)
            max_profit_money = []
            max_loss_money = []
        for n in range(0, len(money_list_all)):
            # 找最大的 + profit_data_final = []
            if len(profit_data_2[n]) == 0:
                profit_data_final.append(0)
            else:
                profit_data_final.append(max(profit_data_2[n]))
            if len(loss_data_2[n]) == 0:
                loss_data_final.append(0)
            else:
                loss_data_final.append(max(loss_data_2[n]))
        for n in range(0, len(money_list_all)):
            # 單筆最 高,低 報酬   分母-->0   ???
            for x in range(0, len(profit_data_2[n])):
                aa = round((profit_data_2[n][x] / max_profit_2[n][x]) * 100, 2)
                max_profit.append(aa)
            for x in range(0, len(loss_data_2[n])):
                bb = round((loss_data_2[n][x] / max_loss_2[n][x]) * 100, 2)
                max_loss.append(bb)
            max_profit_list.append(max_profit)
            max_loss_list.append(max_loss)
            max_profit = []
            max_loss = []
            print()
            print('max_profit_list')
            print(max_profit_list)
            print('max_loss_list')
            print(max_loss_list)
            print()
        for n in range(0, len(money_list_all)):
            # 找最大的 + max_profit_final = []
            if len(max_profit_list[n]) == 0:
                max_profit_final.append(0)
            else:
                max_profit_final.append(max(max_profit_list[n]))
            if len(max_loss_list[n]) == 0:
                max_loss_final.append(0)
            else:
                max_loss_final.append(max(max_loss_list[n]))
        a = [11.42, 8.63, 5.71, 8.52, 6.2, 10.2, 11.05, 9.37, 8.70, 7.29, 8.6, 10.7]  # max_profit_list[0]
        b = [8.9, 7.23, 7.81, 8.2, 8.65, 9.43, 7.1, 6.4, 7.89, 7.31, 8.5, 7.63]  # max_profit_list[1]
        print('gross_profit_list')
        print(gross_profit_list)
        print('gross_loss_list')
        print(gross_loss_list)
        print('stock_name_list')
        print(stock_name_list)
        print('times_list')
        print(times_list)
        print('money_list_all')
        print(money_list_all)
        print('profit_data_2')
        print(profit_data_2)
        print('loss_data_2')
        print(loss_data_2)
        print('max_profit_2')
        print(max_profit_2)
        print('max_loss_2')
        print(max_loss_2)
        return render_to_response('back2.html', {'a': a, 'b': b, 'loginstatus': loginstatus, 'name': name,
                                                 'stock_name': stock_name_list, 'times': times_list,
                                                 'c1': range(0, len(stock_final)), 'money_final': money_final_list,
                                                 'money_begin': money_begin_list, 'gross_profit': gross_profit_list,
                                                 'gross_loss': gross_loss_list, 'gross': gross_list, 'gain': gain_list,
                                                 'total_1': total_1_list, 'total_3': total_3_list,
                                                 'total_4': total_4_list,
                                                 'total_5': total_5_list, 'profit_data': profit_data_final,
                                                 'loss_data': loss_data_final, 'max_profit': max_profit_final,
                                                 'max_loss': max_loss_final, 'total_6_list': total_6_list})
    list1 = []
    list2 = []
    list3 = []
    list4 = []
    list5 = []
    list1 = stock_list.filter(list_id='1')
    list2 = stock_list.filter(list_id='2')
    list3 = stock_list.filter(list_id='3')
    list4 = stock_list.filter(list_id='4')
    list5 = stock_list.filter(list_id='5')
    num1 = len(list1)
    return render_to_response('back.html', {'list1': list1, 'list2': list2, 'list3': list3, 'list4': list4,
                                            'list5': list5, 'num1': num1})

# --期貨專區
def stock(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass

    if request.method == 'POST':
        s_num = request.POST.get('search', '2330')
        id = s_num[0:4]
        # share = Share(id+'.TW')
        # price = share.get_price()
        # change = share.get_change()
        # prev_close = share.get_prev_close()
        # change_in_percent = round(float(change)/float(prev_close), ndigits=2)*100
        # volume = share.get_volume()
        capital = round(float(RobotInformation.objects.get(stock_id=id).co_capital), ndigits=2)
        category_id = RobotInformation.objects.get(stock_id=id).category
        industry = RobotCategory.objects.get(category_id=category_id).category_name
        set = []
        set2 = []
        all = RobotMonthrevenue.objects.filter(stock_id=id)
        s_price = RobotTransactionInfo.objects.filter(stock_id=id)
        for n in all:
            n.month_revenue = float(n.month_revenue)
            set.append(n.month_revenue)
        for i in s_price[0:36]:
            i.the_close = float(i.the_close)
            set2.append(i.the_close)
        a = []
        for i in range(41, 51):
            a.append(RobotNews2330.objects.get(id=i))

        #####股利政策
        set3 = []
        data = RobotDividendPolicy.objects.filter(stock_id=id)
        try:
            for i in range(0, 9):
                set3.append(data[i])
        except:
            pass
        '''
        for i in range(0, 9):
        set3.append(data[i])
        '''
        cash = []
        for i in data:
            i.cash_dividend = round(float(i.cash_dividend), ndigits=2)
            cash.append(i.cash_dividend)
        stocks = []
        for i in data:
            i.stock_dividend = round(float(i.stock_dividend), ndigits=2)
            stocks.append(i.stock_dividend)
        cp = []
        cp2 = []
        c = RobotTransactionInfo.objects.filter(stock_id=id)
        for i in c:
            i.the_close = round(float(i.the_close), ndigits=2)
            cp.append(i.the_close)
        for i in range(0, 96):
            cp2.append(cp[i])
        ##################融資融券
        set4 = []
        data1 = RobotMargin.objects.filter(stock_id=id)
        for i in range(0, 5):
            set4.append(data1[i])
        cd = []
        cd2 = []
        d = RobotTransactionInfo.objects.filter(stock_id=id)
        for i in d:
            i.the_close = round(float(i.the_close), ndigits=2)
            cd.append(i.the_close)
        for i in range(160, 2, -1):
            cd2.append(cd[i])
        mb = []
        data2 = RobotMargin.objects.filter(date__contains='2016', stock_id=id)
        for i in data2:
            if (i.margin_balance == '--'):
                i.margin_balance = 0
            else:
                i.margin_balance = round(float(i.margin_balance), ndigits=2)
            mb.append(i.margin_balance)  # 融資餘額
        mb2 = []
        for i in data2:
            if (i.stockloan_balance == '--'):
                i.stockloan_balance = 50
            else:
                i.stockloan_balance = round(float(i.stockloan_balance), ndigits=2)
            mb2.append(i.stockloan_balance)  # 融券餘額
        print(change)
        pe, score, month_growth, year_growth = RobotPe.objects.filter(stock_id=id).order_by(
            '-date').first().pe_for_four_season, 0, Ratio2_Q.objects.filter(
            stock_id=id).first().revenue_growth_ratio, Ratio2.objects.filter(stock_id=id).first().revenue_growth_ratio
        if float(RobotRatio4Q.objects.filter(stock_id=id).first().debt_ratio) < 0.5:
            score = 5
        else:
            score = 3
        # k_diagram_4(id)
        return render_to_response('stock.html',
                                  {'pe': pe, 'score': score, 'month_growth': month_growth, 'year_growth': year_growth,
                                   'cd2': cd2, 'mb': mb, 'mb2': mb2, 'cash': cash, 'stocks': stocks, 'cp': cp2,
                                   'set': set, 'set2': set2, 'stock_name': Information.objects.get(stock_id=id).co_name,
                                   'id': Information.objects.get(stock_id=id).stock_id, 'price': price,
                                   'change_in_percent': change_in_percent, 'change': change, 'volume': volume,
                                   'capital': capital, 'industry': industry, 'news': a, 'loginstatus': loginstatus,
                                   'name': name})
    ######################
    id = request.GET.get('stock_id', '2330')  # 選股有查看資訊功能
    # share = Share(id+'.TW')
    # price = share.get_price()
    # change = share.get_change()
    # prev_close = share.get_prev_close()
    # change_in_percent = round(float(change)/float(prev_close), ndigits=2)*100
    # volume = share.get_volume()
    capital = round(float(RobotInformation.objects.get(stock_id=id).co_capital), ndigits=2)
    category_id = RobotInformation.objects.get(stock_id=id).category
    industry = RobotCategory.objects.get(category_id=category_id).category_name
    set = []
    set2 = []
    all = RobotMonthrevenue.objects.filter(stock_id=id)
    s_price = RobotTransactionInfo.objects.filter(stock_id=id)
    for n in all:
        n.month_revenue = float(n.month_revenue)
        set.append(n.month_revenue)
    for i in s_price[0:36]:
        i.the_close = float(i.the_close)
        set2.append(i.the_close)
    a = []
    for i in range(41, 51):
        a.append(RobotNews2330.objects.get(id=i))

    #####股利政策
    set3 = []
    data = RobotDividendPolicy.objects.filter(stock_id=id)
    '''for i in range(0, 9):
        set3.append(data[i])'''
    try:
        for i in range(0, 9):
            set3.append(data[i])
    except:
        pass
    cash = []
    for i in data:
        i.cash_dividend = round(float(i.cash_dividend), ndigits=2)
        cash.append(i.cash_dividend)
    stocks = []
    for i in data:
        i.stock_dividend = round(float(i.stock_dividend), ndigits=2)
        stocks.append(i.stock_dividend)
    cp = []
    cp2 = []
    c = RobotTransactionInfo.objects.filter(stock_id=id)
    for i in c:
        i.the_close = round(float(i.the_close), ndigits=2)
        cp.append(i.the_close)
    for i in range(0, 96):
        cp2.append(cp[i])
    ##################融資融券
    set4 = []
    data1 = RobotMargin.objects.filter(stock_id=id)
    for i in range(0, 5):
        set4.append(data1[i])
    cd = []
    cd2 = []
    d = RobotTransactionInfo.objects.filter(stock_id=id)
    for i in d:
        i.the_close = round(float(i.the_close), ndigits=2)
        cd.append(i.the_close)
    for i in range(160, 2, -1):
        cd2.append(cp[i])
    mb = []
    data2 = RobotMargin.objects.filter(date__contains='2016', stock_id=id)
    for i in data2:
        if (i.margin_balance == '--'):
            i.margin_balance = 0
        else:
            i.margin_balance = round(float(i.margin_balance), ndigits=2)
        mb.append(i.margin_balance)  # 融資餘額
    mb2 = []
    for i in data2:
        if (i.stockloan_balance == '--'):
            i.stockloan_balance = 50
        else:
            i.stockloan_balance = round(float(i.stockloan_balance), ndigits=2)
        mb2.append(i.stockloan_balance)  # 融券餘額
    # k_diagram_4(id)
    #################### K線圖
    pe, score, month_growth, year_growth = RobotPe.objects.filter(stock_id=id).order_by(
        '-date').first().pe_for_four_season, 0, RobotRatio2Q.objects.filter(
        stock_id=id).first().revenue_growth_ratio, RobotRatio2.objects.filter(stock_id=id).first().revenue_growth_ratio
    if float(RobotRatio4Q.objects.filter(stock_id=id).first().debt_ratio) < 0.5:
        score = 5
    else:
        score = 3
    # return render_to_response('stock.html', {'pe': float(pe),'score': score, 'month_growth': float(month_growth), 'year_growth': float(year_growth),'cd2': cd2, 'mb': mb, 'mb2': mb2, 'cash': cash,'stocks': stocks,'cp': cp2, 'set': set, 'set2': set2, 'stock_name': RobotInformation.objects.get(stock_id=id).co_name, 'id': RobotInformation.objects.get(stock_id=id).stock_id, 'price': price, 'change_in_percent': change_in_percent, 'change': change, 'volume': volume, 'capital': capital, 'industry': industry, 'news': a,'loginstatus': loginstatus, 'name': name})
    return render_to_response('stock.html', {'pe': float(pe), 'score': score, 'month_growth': float(month_growth),
                                             'year_growth': float(year_growth), 'cd2': cd2, 'mb': mb, 'mb2': mb2,
                                             'cash': cash, 'stocks': stocks, 'cp': cp2, 'set': set, 'set2': set2,
                                             'stock_name': RobotInformation.objects.get(stock_id=id).co_name,
                                             'id': RobotInformation.objects.get(stock_id=id).stock_id,
                                             'capital': capital, 'industry': industry, 'news': a,
                                             'loginstatus': loginstatus, 'name': name})


# 即時資料
def recent(request):
    return render(request, 'recent.html')


# --能跑出資料庫資料
def index(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    if name != '':
        member_id = RobotMember.objects.get(member_name=name).member_id
        rank2_stock_name, rank_stock_name, rank3_stock_name, rank4_stock_name, info = [], [], [], [], []
        res = RobotDiscuss.objects.order_by('-like')
        res_3 = RobotDiscuss.objects.order_by('-date', '-time')
        hot = RobotYahooNew.objects.order_by('-date')
        rank = RobotTransactionInfo.objects.filter(date='20160826').order_by('-change')[:5]
        rank2 = RobotTransactionInfo.objects.filter(date='20160826').order_by('-vol')[:5]
        rank3 = RobotCorporate.objects.filter(date='20160826').order_by('-foreign_net')[:5]
        rank4 = RobotCorporate.objects.filter(date='20160826').order_by('-trust_net')[:5]
        list_name = RobotTrackStock.objects.filter(member_id=member_id).order_by('list_name').values(
            'list_name').distinct()
        list2_name = []
        try:
            list2_name = list_name.exclude(list_name=RobotTrackStock.objects.filter(member_id=member_id).order_by(
                'list_name').values('list_name').distinct().first()['list_name'])
        except:
            pass
        track = RobotTrackStock.objects.filter(member_id=member_id)

        for i in rank:
            rank_stock_name.append(RobotInformation.objects.get(stock_id=i.stock_id).co_name)
        for i in rank2:
            rank2_stock_name.append(RobotInformation.objects.get(stock_id=i.stock_id).co_name)
        for i in rank3:
            rank3_stock_name.append(RobotInformation.objects.get(stock_id=i.stock_id).co_name)
        for i in rank4:
            rank4_stock_name.append(RobotInformation.objects.get(stock_id=i.stock_id).co_name)
        for i in track:
            s = Share(i.stock_id + '.TW')
            s1, s2, s3, s4 = s.get_price(), s.get_change(), s.get_percent_change(), s.get_volume()
            if s1 is None:
                s1 = 0
            if s2 is None:
                s2 = 0
            if s3 is None:
                s3 = 0
            if s4 is None:
                s4 = 0
            industry_id = RobotInformation.objects.get(stock_id=i.stock_id).category
            indusry_name = RobotCategory.objects.get(category_id=industry_id).category_name
            capital = RobotInformation.objects.get(stock_id=i.stock_id).co_capital
            info.append({'list_name': i.list_name, 'stock_id': i.stock_id, 'stock_name': i.stock_name, 'price': s1,
                         'change': s2, 'change_percent': s3, 'vol': s4, 'capital': capital, 'industry': indusry_name})
        return render_to_response('recent.html',
                                  {'loginstatus': loginstatus, 'name': name, 'res': res, 'res_3': res_3, 'rank': rank,
                                   'rank2': rank2, 'hot': hot, 'rank3': rank3, 'rank4': rank4,
                                   'rank_name': rank_stock_name,
                                   'rank2_name': rank2_stock_name, 'rank3_name': rank3_stock_name,
                                   'rank4_name': rank4_stock_name,
                                   'list_name': list_name, 'list2_name': list2_name, 'track': info})
    else:
        rank2_stock_name, rank_stock_name, rank3_stock_name, rank4_stock_name, info = [], [], [], [], []
        res = RobotDiscuss.objects.order_by('-like')
        res_3 = RobotDiscuss.objects.order_by('-date', '-time')
        hot = RobotYahooNew.objects.order_by('-date')
        rank = RobotTransactionInfo.objects.filter(date='20160826').order_by('-change')[:5]
        rank2 = RobotTransactionInfo.objects.filter(date='20160826').order_by('-vol')[:5]
        rank3 = RobotCorporate.objects.filter(date='20160826').order_by('-foreign_net')[:5]
        rank4 = RobotCorporate.objects.filter(date='20160826').order_by('-trust_net')[:5]
        for i in rank:
            rank_stock_name.append(RobotInformation.objects.get(stock_id=i.stock_id).co_name)
        for i in rank2:
            rank2_stock_name.append(RobotInformation.objects.get(stock_id=i.stock_id).co_name)
        for i in rank3:
            rank3_stock_name.append(RobotInformation.objects.get(stock_id=i.stock_id).co_name)
        for i in rank4:
            rank4_stock_name.append(RobotInformation.objects.get(stock_id=i.stock_id).co_name)
        return render_to_response('recent.html',
                                  {'loginstatus': loginstatus, 'name': name, 'res': res, 'res_3': res_3, 'rank': rank,
                                   'rank2': rank2, 'hot': hot, 'rank3': rank3, 'rank4': rank4,
                                   'rank_name': rank_stock_name,
                                   'rank2_name': rank2_stock_name, 'rank3_name': rank3_stock_name,
                                   'rank4_name': rank4_stock_name,
                                   })


# EDITOR

# 智能機器人
def stock_analysis(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    link = request.GET.get('link', 0)
    if link == '1_1':
        return render_to_response('stock_anacon.html', {'loginstatus': loginstatus, 'name': name})
    elif link == '1_10':
        return render_to_response('stock_anacon1.html', {'loginstatus': loginstatus, 'name': name})
    return render_to_response('stock_ana.html', {'loginstatus': loginstatus, 'name': name})


# --預知未來型
def predict(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        return HttpResponseRedirect('/login/?back=未來型預測')
    category_id = RobotMember.objects.get(member_name=name).type
    cname = RobotFqType.objects.get(type_id=category_id).type_name
    if request.method == 'POST':
        stock = request.POST.get('stock', '')
        stock = stock[0:4]
        period = request.POST.get('myCheckBox', '')
        item1 = request.POST.get('myCheckBox2', '')
        paragraph1 = '本系統預測功能使用線性回歸模型來為使用者預測每股盈餘，使用者可參考此預測結果來決定要買進或賣出股票'
        if period == 'season' and item1 == 'profit':
            predict, search, past, industry_avg, std, category_name, score, next_season = predict_eps_season(stock)
            return render_to_response('predict2.html', {'paragraph1': paragraph1, 'predict_type': '獲利能力', 'id': stock,
                                                        'predict': predict, 'search': search, 'past': past,
                                                        'industry_avg': industry_avg, 'std': std,
                                                        'category_name': category_name, 'score': score,
                                                        'next': next_season, 'season': '季', 'loginstatus': loginstatus,
                                                        'name': name})
        if period == 'year' and item1 == 'profit':
            predict, search, past, industry_avg, std, category_name, score, next_year = predict_eps_year(stock)
            return render_to_response('predict2.html', {'paragraph1': paragraph1, 'predict_type': '獲利能力', 'id': stock,
                                                        'predict': predict, 'search': search, 'past': past,
                                                        'industry_avg': industry_avg, 'std': std,
                                                        'category_name': category_name, 'score': score,
                                                        'next': next_year, 'season': '年', 'loginstatus': loginstatus,
                                                        'name': name})

    return render_to_response('predict.html', {'cname': cname, 'loginstatus': loginstatus, 'name': name})

# --健康診斷型
def stock_analysis(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    link = request.GET.get('link', 0)
    if link == '1_1':
        return render_to_response('stock_anacon.html', {'loginstatus': loginstatus, 'name': name})
    elif link == '1_10':
        return render_to_response('stock_anacon1.html', {'loginstatus': loginstatus, 'name': name})
    return render_to_response('stock_ana.html', {'loginstatus': loginstatus, 'name': name})

# --推薦好股型（開不出來
def gep(request):
    return render(request, "gep1.html")

# --買賣型

def five(request):
    return render(request, "f.html")


# --投資組合推薦 (開不出來


# 指標專區

def economic_term(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    c_1 = RobotEconomic.objects.filter(category='獲利能力')
    c_2 = RobotEconomic.objects.filter(category='安全性')
    c_3 = RobotEconomic.objects.filter(category='成長力')
    c_4 = RobotEconomic.objects.filter(category='財務報表')
    return render_to_response('dict.html',
                              {'name': name, 'loginstatus': loginstatus, 'c_1': c_1, 'c_2': c_2, 'c_3': c_3,
                               'ca_1': c_1[0].category, 'ca_2': c_2[0].category, 'ca_3': c_3[0].category,
                               'c_4': c_4, 'ca_4': c_4[0].category})


# 下單機
def tech(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass

    return render_to_response('tech.html', {'name': name, 'loginstatus': loginstatus})


# 新手專區
# --討論區
def get_article(request):#熱門文章 最新文章 最新回復
    today = datetime.datetime.now().strftime('%Y/%m/%d')
    count = Discuss.objects.filter(date=today).count()
    count2 = Discuss.objects.all().count()
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    a = []
    res = Discuss.objects.order_by('-like').all()
    for i in range(0, 4):
        a.append(res[i])
    res_2 = Comment.objects.order_by('-date', '-time')
    b = []
    for i in range(0, 4):
        b.append(res_2[i])
    res_3 = Discuss.objects.order_by('-date', '-time')
    c = []
    for i in range(0, 4):
        c.append(res_3[i])
    request.session['post_page'] = '1'
    page = request.session['post_page']
    d = []
    res_4 = Discuss.objects.order_by('-reply_times').filter(theme = '投資理財')
    for i in range(0, 15):
        d.append(res_4[i])
    e = []
    res_5 = Discuss.objects.order_by('-reply_times').filter(theme = '股票相關')
    for i in range(0, 15):
        e.append(res_5[i])
    f = []
    res_6 = Discuss.objects.order_by('-reply_times').filter(theme = '機器人投顧')
    for i in range(0, 15):
        f.append(res_6[i])
    return render_to_response('chat.html', {'count': count, 'count2': count2,'hot': a, 'latest_reply': b,'latest': c,'article': d, 'article_2': e, 'article_3': f,'page': page, 'name': name, 'loginstatus': loginstatus})

# --回傳內容
def content(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    id = request.GET.get('id', 0)
    id = int(id)
    res = RobotDiscuss.objects.get(discuss_id=id)
    comment = RobotComment.objects.filter(discuss_id=id)
    return render_to_response('chatcon.html',
                              {'article': res, 'comment': comment, 'id': id, 'name': name, 'loginstatus': loginstatus})


def post_page_1(request):
    today = datetime.now().strftime('%Y/%m/%d')
    count = RobotDiscuss.objects.filter(date=today).count()
    count2 = RobotDiscuss.objects.all().count()
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    a = []
    res = RobotDiscuss.objects.order_by('-like').all()
    for i in range(0, 4):
        a.append(res[i])
    res_2 = RobotComment.objects.order_by('-date', '-time')
    b = []
    for i in range(0, 4):
        b.append(res_2[i])
    res_3 = RobotDiscuss.objects.order_by('-date', '-time')
    c = []
    for i in range(0, 4):
        c.append(res_3[i])
    request.session['post_page'] = '1'
    page = request.session['post_page']
    d = []
    res_4 = RobotDiscuss.objects.order_by('-reply_times').filter(theme='投資理財')
    for i in range(0, 15):
        d.append(res_4[i])
    e = []
    res_5 = RobotDiscuss.objects.order_by('-reply_times').filter(theme='股票相關')
    for i in range(0, 15):
        e.append(res_5[i])
    f = []
    res_6 = RobotDiscuss.objects.order_by('-reply_times').filter(theme='機器人投顧')
    for i in range(0, 15):
        f.append(res_6[i])
    return render_to_response('chat.html',
                              {'count': count, 'count2': count2, 'page': page, 'article': d, 'article_2': e,
                               'article_3': f, 'hot': a, 'latest_reply': b, 'latest': c, 'name': name,
                               'loginstatus': loginstatus})


def post_page_2(request):
    today = datetime.now().strftime('%Y/%m/%d')
    count = RobotDiscuss.objects.filter(date=today).count()
    count2 = RobotDiscuss.objects.all().count()
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    a = []
    res = RobotDiscuss.objects.order_by('-like').all()
    for i in range(0, 4):
        a.append(res[i])
    res_2 = RobotComment.objects.order_by('-date', '-time')
    b = []
    for i in range(0, 4):
        b.append(res_2[i])
    res_3 = RobotDiscuss.objects.order_by('-date', '-time')
    c = []
    for i in range(0, 4):
        c.append(res_3[i])
    request.session['post_page'] = '2'
    page = request.session['post_page']
    d = []
    res_4 = RobotDiscuss.objects.order_by('-reply_times').filter(theme='投資理財')
    for i in range(15, 30):
        d.append(res_4[i])
    e = []
    res_5 = RobotDiscuss.objects.order_by('-reply_times').filter(theme='股票相關')
    for i in range(15, 30):
        e.append(res_5[i])
    f = []
    res_6 = RobotDiscuss.objects.order_by('-reply_times').filter(theme='機器人投顧')
    for i in range(15, 30):
        f.append(res_6[i])
    return render_to_response('chat.html',
                              {'count': count, 'count2': count2, 'page': page, 'article_2': e, 'article_3': f,
                               'article': d, 'hot': a, 'latest_reply': b, 'latest': c, 'name': name,
                               'loginstatus': loginstatus})


def post_page_3(request):
    today = datetime.now().strftime('%Y/%m/%d')
    count = RobotDiscuss.objects.filter(date=today).count()
    count2 = RobotDiscuss.objects.all().count()
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    a = []
    res = RobotDiscuss.objects.order_by('-like').all()
    for i in range(0, 4):
        a.append(res[i])
    res_2 = RobotComment.objects.order_by('-date', '-time')
    b = []
    for i in range(0, 4):
        b.append(res_2[i])
    res_3 = RobotDiscuss.objects.order_by('-date', '-time')
    c = []
    for i in range(0, 4):
        c.append(res_3[i])
    request.session['post_page'] = '3'
    page = request.session['post_page']
    d = []
    res_4 = RobotDiscuss.objects.order_by('-reply_times').filter(theme='投資理財')
    for i in range(30, 45):
        d.append(res_4[i])
    e = []
    res_5 = RobotDiscuss.objects.order_by('-reply_times').filter(theme='股票相關')
    for i in range(30, 45):
        e.append(res_5[i])
    f = []
    res_6 = RobotDiscuss.objects.order_by('-reply_times').filter(theme='機器人投顧')
    for i in range(30, 45):
        f.append(res_6[i])
    return render_to_response('chat.html',
                              {'count': count, 'count2': count2, 'page': page, 'article_2': e, 'article_3': f,
                               'article': d, 'hot': a, 'latest_reply': b, 'latest': c, 'name': name,
                               'loginstatus': loginstatus})


def post_next(request):  # 下一頁 check
    page = request.session['post_page']
    type = request.GET.get('type', 0)
    if page is '1':
        return HttpResponseRedirect('/post_page_2/')
    if page is '2':
        return HttpResponseRedirect('/post_page_3/')
    if page is '3':
        return HttpResponseRedirect('/post_page_3/')


def post_prev(request):  # 上一頁 check
    page = request.session['post_page']
    type = request.GET.get('type', 0)
    if page is '1':
        return HttpResponseRedirect('/post_page_1/')
    if page is '2':
        return HttpResponseRedirect('/post_page_1/')
    if page is '3':
        return HttpResponseRedirect('/post_page_2/')


def like(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    if request.method == 'POST':
        id = request.POST.get('id', 0)
        likes = RobotDiscuss.objects.get(discuss_id=id).like
        RobotDiscuss.objects.filter(discuss_id=id).update(like=likes + 1)
        res = RobotDiscuss.objects.get(discuss_id=id)
        comment = RobotComment.objects.filter(discuss_id=id)
        return render_to_response('chatcon.html', {'article': res, 'comment': comment, 'id': id, 'name': name,
                                                   'loginstatus': loginstatus})


def issued(request):
    return render(request, 'post.html')


def chat_search(request):
    return render(request, 'chat_search')


# 會員

def member(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass

    return render_to_response('member2.html', {'name': name, 'loginstatus': loginstatus})


def mem_home(request):  # check
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    return render_to_response('member2.html', {'loginstatus': loginstatus, 'name': name})


# def member_news(request):
#     name = ''
#     loginstatus = False
#     member = ''
#     try:
#          name = request.session['name']
#          member = RobotMember.objects.get(member_name=name).member_id
#          loginstatus = True
#     except:
#         return HttpResponseRedirect('/login/?back=My_News')
#     # member = '1'
#     stock = RobotTrackStock.objects.filter(member_id=member)
#     tra = []
#     tra1 = [] # 漲跌
#     tra2 = [] # 漲跌幅
#     inf = []
#     cate = []
#     range1 = []
#     list, l0, l1, l2, l3, l4, l5 = [], [], [], [], [], [], []
#     # 投資組合清單
#     try:
#        l0 = RobotTrackStock.objects.filter(member_id = member, list_id = '0')
#        list.append(l0[0])
#     except:
#        #l0 = 0
#        #list.append(l0)
#        pass
#     try:
#        l1 = RobotTrackStock.objects.filter(member_id = member, list_id = '1')
#        list.append(l1[0])
#     except:
#        #l1 = 0
#        #list.append(l1)
#        pass
#     try:
#        l2 = RobotTrackStock.objects.filter(member_id = member, list_id = '2')
#        list.append(l2[0])
#     except:
#        #l2 = 0
#        #list.append(l2)
#        pass
#     try:
#        l3 = RobotTrackStock.objects.filter(member_id = member, list_id = '3')
#        list.append(l3[0])
#     except:
#        #l3 = 0
#        #list.append(l3)
#        pass
#     try:
#        l4 = RobotTrackStock.objects.filter(member_id = member, list_id = '4')
#        list.append(l4[0])
#     except:
#        #l4 = 0
#        #list.append(l4)
#        pass
#     try:
#        l5 = RobotTrackStock.objects.filter(member_id = member, list_id = '5')
#        list.append(l5[0])
#     except:
#        #l5 = 0
#        #list.append(l5)
#        pass
#     #list = [l0[0], l1[0], l2[0], l3[0], l4[0], l5[0]]
#
#     # 當日的交易資訊-- ALL
#     tr_list = request.POST.get('list', '')
#     if tr_list == 'ALL' or tr_list == '':
#         for n in range(0, len(stock)):
#             tra.append(RobotTransactionInfo.objects.get(stock_id=stock[n].stock_id, date='20160826'))
#             tra1.append(float(RobotTransactionInfo.objects.get(stock_id=stock[n].stock_id, date='20160826').change))
#             tra2.append(float(RobotTransactionInfo.objects.get(stock_id=stock[n].stock_id, date='20160826').change_percent))
#             a = RobotInformation.objects.get(stock_id=stock[n].stock_id)
#             inf.append(a)
#             cate.append(RobotCategory.objects.get(category_id=a.category))
#             range1.append(n)
#         page_2 = request.GET.get('page' , '1')
#         page_2 = int(page_2)
#         track_stock = RobotTrackStock.objects.filter(member_id=member)
#         yahoo = []
#         for news in track_stock:
#             if RobotYahoo.objects.order_by('-date').filter(title__contains=news.stock_name, content__contains=news.stock_name):
#                 for i in RobotYahoo.objects.order_by('-date').filter(title__contains=news.stock_name, content__contains=news.stock_name):
#                     yahoo.append({'category': 'Yahoo!奇摩股市-台盤股勢', 'type': '4', 'title': i.title, 'date': i.date,'time':i.time, 'stock': news.stock_name})
#             if RobotYahooStock.objects.order_by('-date').filter(title__contains=news.stock_name, content__contains=news.stock_name):
#                 for i in RobotYahooStock.objects.order_by('-date').filter(title__contains=news.stock_name, content__contains=news.stock_name):
#                     yahoo.append({'category': 'Yahoo!奇摩股市-個股動態', 'type': '5', 'title': i.title, 'date': i.date,'time':i.time, 'stock': news.stock_name})
#             if RobotYahooTec.objects.order_by('-date').filter(title__contains=news.stock_name, content__contains=news.stock_name):
#                 for i in RobotYahooTec.objects.order_by('-date').filter(title__contains=news.stock_name, content__contains=news.stock_name):
#                     yahoo.append({'category': 'Yahoo!奇摩股市-科技產業', 'type': '6', 'title': i.title, 'date': i.date,'time':i.time, 'stock': news.stock_name})
#             if RobotYahooTra.objects.order_by('-date').filter(title__contains=news.stock_name, content__contains=news.stock_name):
#                 for i in RobotYahooTra.objects.order_by('-date').filter(title__contains=news.stock_name, content__contains=news.stock_name):
#                     yahoo.append({'category': 'Yahoo!奇摩股市-傳統產業', 'type': '7', 'title': i.title, 'date': i.date,'time':i.time, 'stock': news.stock_name})
#             if news.stock_id == '2330':
#                 for i in RobotNews2330.objects.order_by('-date'):
#                     yahoo.append({'category': 'Yahoo!奇摩股市-科技產業', 'type': '2330', 'title': i.title, 'date': i.date,'time':i.time, 'stock': news.stock_name})
#     else:
#         if tr_list == '0':
#             stock = l0
#         elif tr_list == '1':
#             stock = l1
#         elif tr_list == '2':
#             stock = l2
#         elif tr_list == '3':
#             stock = l3
#         elif tr_list == '4':
#             stock = l4
#         print(stock)
#         for n in range(0, len(stock)):
#             print(stock[n].stock_id)
#             tra.append(RobotTransactionInfo.objects.get(stock_id=stock[n].stock_id, date='20160826'))
#             tra1.append(float(RobotTransactionInfo.objects.get(stock_id=stock[n].stock_id, date='20160826').change))
#             tra2.append(float(RobotTransactionInfo.objects.get(stock_id=stock[n].stock_id, date='20160826').change_percent))
#             a = RobotInformation.objects.get(stock_id=stock[n].stock_id)
#             inf.append(a)
#             cate.append(RobotCategory.objects.get(category_id=a.category))
#             range1.append(n)
#         page_2 = request.GET.get('page' , '1')
#         page_2 = int(page_2)
#         track_stock = RobotTrackStock.objects.filter(member_id=member)
#         yahoo = []
#         for news in track_stock:
#             if RobotYahoo.objects.order_by('-date').filter(title__contains=news.stock_name, content__contains=news.stock_name):
#                 for i in RobotYahoo.objects.order_by('-date').filter(title__contains=news.stock_name, content__contains=news.stock_name):
#                     yahoo.append({'category': 'Yahoo!奇摩股市-台盤股勢', 'type': '4', 'title': i.title, 'date': i.date,'time':i.time, 'stock': news.stock_name})
#             if RobotYahooStock.objects.order_by('-date').filter(title__contains=news.stock_name, content__contains=news.stock_name):
#                 for i in RobotYahooStock.objects.order_by('-date').filter(title__contains=news.stock_name, content__contains=news.stock_name):
#                     yahoo.append({'category': 'Yahoo!奇摩股市-個股動態', 'type': '5', 'title': i.title, 'date': i.date,'time':i.time, 'stock': news.stock_name})
#             if RobotYahooTec.objects.order_by('-date').filter(title__contains=news.stock_name, content__contains=news.stock_name):
#                 for i in RobotYahooTec.objects.order_by('-date').filter(title__contains=news.stock_name, content__contains=news.stock_name):
#                     yahoo.append({'category': 'Yahoo!奇摩股市-科技產業', 'type': '6', 'title': i.title, 'date': i.date,'time':i.time, 'stock': news.stock_name})
#             if RobotYahooTra.objects.order_by('-date').filter(title__contains=news.stock_name, content__contains=news.stock_name):
#                 for i in RobotYahooTra.objects.order_by('-date').filter(title__contains=news.stock_name, content__contains=news.stock_name):
#                     yahoo.append({'category': 'Yahoo!奇摩股市-傳統產業', 'type': '7', 'title': i.title, 'date': i.date,'time':i.time, 'stock': news.stock_name})
#             if news.stock_id == '2330':
#                 for i in RobotNews2330.objects.order_by('-date'):
#                     yahoo.append({'category': 'Yahoo!奇摩股市-科技產業', 'type': '2330', 'title': i.title, 'date': i.date,'time':i.time, 'stock': news.stock_name})
#
#
#
#     #a = Transaction_info.objects.all().aggregate(Min('the_close'))
#     #print(a)
#     paginator = Paginator(yahoo, 10)
#     try:
#         news = paginator.page(page_2)
#     except PageNotAnInteger:
#         news = paginator.page(1)
#     except EmptyPage:
#         news = paginator.page(paginator.num_pages)
#     return render_to_response('member_news_2.html', {'tra_data': tra, 'tra1': tra1, 'tra2': tra2, 'inf_data': inf, 'cate': cate,
#                                                'range1': range1, 'news': news, 'name': name, 'loginstatus': loginstatus, 'list': list,'tr_list': tr_list})


# --新聞首頁

# --忘記密碼

def modifypassword(request):
    try:
        username = request.session['userName']
    except:
        return HttpResponseRedirect('/login/?back=修改密碼')
    if request.method == 'POST':
        newpassword = request.POST.get('newpass', '')
        check = request.POST.get('pass', '')
        check_2 = RobotMember.objects.filter(password=newpassword)
        if check_2:
            wrong = '此密碼已被使用'
            return render_to_response('mo_pass.html', {'wrong': wrong})
        elif newpassword == check:
            RobotMember.objects.filter(email=username).update(password=newpassword)
            return render_to_response('login.html')
    return render_to_response('mo_pass.html')


def modify(request):
    try:
        username = request.session['userName']
        result = RobotMember.objects.get(email=username)
    except:
        return HttpResponseRedirect('/login/?back=修改基本資料')
    if request.method == 'POST':
        name = request.POST.get('name', '')
        mail = request.POST.get('mail', '')
        phone = request.POST.get('phone', '')
        RobotMember.objects.filter(email=username).update(member_name=name, email=mail, phone_num=phone)
        request.session['name'] = name
        request.session['userName'] = mail
        return render_to_response('login.html')
    return render_to_response('modify.html', {'member': result})


# 損益表
def income_statement(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    identity = request.GET.get('id', '2330')
    data_2 = RobotIncomeStatementQ.objects.filter(stock_id=identity)
    sets = []
    for i in range(0, 8):
        sets.append(data_2[i])
    #     # share = Share(identity+'.TW')
    #     # price = share.get_price()
    #     # change = share.get_change()
    #     # prev_close = share.get_prev_close()
    #     # change_in_percent = round(float(change)/float(prev_close), ndigits=2)*100
    #     # volume = share.get_volume()
    capital = RobotInformation.objects.get(stock_id=identity).co_capital
    category_id = RobotInformation.objects.get(stock_id=identity).category
    industry = RobotCategory.objects.get(category_id=category_id).category_name
    #     # return render_to_response('inc_sta.html', {'stock_name': RobotInformation.objects.get(stock_id=identity).co_name, 'stock': sets, 'price': price, 'change_in_percent': change_in_percent, 'change': change, 'volume': volume, 'capital': capital, 'industry': industry, 'id': identity, 'name': name, 'loginstatus': loginstatus})
    return render_to_response('inc_sta.html',
                              {'stock_name': RobotInformation.objects.get(stock_id=identity).co_name, 'stock': sets,
                               'capital': capital, 'industry': industry, 'id': identity, 'name': name,
                               'loginstatus': loginstatus})


# 現金流量表
def cash_flow_statement(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    identity = request.GET.get('id', '2330')
    set = []
    data_2 = RobotCashFlowsQ.objects.filter(stock_id=identity)
    for i in range(0, 8):
        set.append(data_2[i])
    # share = Share(identity+'.TW')
    # price = share.get_price()
    # change = share.get_change()
    # prev_close = share.get_prev_close()
    # change_in_percent = round(float(change)/float(prev_close), ndigits=2)*100
    # volume = share.get_volume()
    capital = RobotInformation.objects.get(stock_id=identity).co_capital
    category_id = RobotInformation.objects.get(stock_id=identity).category
    industry = RobotCategory.objects.get(category_id=category_id).category_name
    # return render_to_response('cash_flow.html', {'stock_name': RobotInformation.objects.get(stock_id=identity).co_name, 'price': price, 'change_in_percent': change_in_percent, 'change': change, 'volume': volume, 'capital': capital, 'industry': industry,'stosk_2': set, 'id': identity, 'name': name, 'loginstatus': loginstatus})
    return render_to_response('cash_flow.html', {'stock_name': RobotInformation.objects.get(stock_id=identity).co_name,
                                                 'capital': capital, 'industry': industry, 'stosk_2': set,
                                                 'id': identity, 'name': name, 'loginstatus': loginstatus})


# 股票代碼查詢
def stock_choice(request):
    # 列出所有產業
    stock_a1 = []  # 上市產業:28個
    stock_a2 = []
    stock_a3 = []
    stock_b1 = []  # 上櫃產業:25個
    stock_b2 = []
    stock_b3 = []
    stock_a = []  # 上市所有股票
    stock_b = []  # 上櫃所有股票
    status = False

    # 前端產業選項用a帶參數id, name
    stock_id = request.GET.get('id', 0)  # 傳到stock.html
    stock_name = request.GET.get('name', 0)  # 哪個產業  傳到stock.html

    type = request.GET.get('c', 0)  # 上市or上櫃
    stock_number = request.GET.get('s_num', 0)  # 顯示在查詢的input
    '''
    <tr>
    {% for stock in a1 %}  要寫三次(有三列)
      <td><a href="/choice/?id={{ stock.id }}&&name={{ stock.name }}&&c=1(上市)/2(上櫃)">{{ stock.name }}</a></td>
    {% endfor %}
    </tr>
    '''

    for n in range(1, 11):  # 10筆一列放入上市
        stock_a1.append(RobotCategoryA.objects.get(cat_id=n))
    for n in range(11, 21):
        stock_a2.append(RobotCategoryA.objects.get(cat_id=n))
    for n in range(21, 29):
        stock_a3.append(RobotCategoryA.objects.get(cat_id=n))
    for n in range(1, 11):  # 10筆一列放入上櫃
        stock_b1.append(RobotCategoryB.objects.get(cat_id=n))
    for n in range(11, 21):
        stock_b2.append(RobotCategoryB.objects.get(cat_id=n))
    for n in range(21, 26):
        stock_b3.append(RobotCategoryB.objects.get(cat_id=n))

    if type is '1':  # 上市找產業的所有股票
        stock_a = RobotListedShares.objects.filter(industry__contains=stock_name)

    elif type is '2':  # 上櫃找產業的所有股票
        stock_b = RobotOverTheCounterShares.objects.filter(industry__contains=stock_name)

    return render_to_response('look.html', {'a': stock_a, 'b': stock_b, 'a1': stock_a1, 'a2': stock_a2, 'a3': stock_a3,
                                            'b1': stock_b1, 'b2': stock_b2, 'b3': stock_b3, 'status': status,
                                            'stock_number': stock_number, 'type': type})

#
#
#
#
# def reply(request):
#     name = ''
#     loginstatus = False
#     try:
#         name = request.session['name']
#         loginstatus = True
#     except:
#         pass
#     date_now = datetime.now().strftime('%Y/%m/%d')
#     time_now = datetime.now().strftime('%H:%M')
#     try:
#         member = request.session['name']
#         if member is not None:
#             if request.method == 'POST':
#                 content = request.POST.get('editor', 0)
#                 discuss_id = request.POST.get('reply', 0)
#                 RobotComment.objects.create(discuss_id=discuss_id, content=content,
#                                        date=date_now, member_id=member, time=time_now)
#                 reply_times = RobotDiscuss.objects.get(discuss_id = discuss_id).reply_times
#                 RobotDiscuss.objects.filter(discuss_id=discuss_id).update(reply_times = reply_times + 1)
#                 res = RobotDiscuss.objects.get(discuss_id=discuss_id)
#                 comment =  RobotComment.objects.filter(discuss_id=discuss_id)
#                 return render_to_response('chatcon.html', {'article': res, 'comment': comment, 'id': discuss_id, 'name': name, 'loginstatus': loginstatus})
#      except:
#      return render_to_response('login.html')
#

def fund2(request):
   name = ''
   loginstatus = False
   try:
        name = request.session['name']
        loginstatus = True
   except:
        return HttpResponseRedirect('/login/?back=資金管理')

   money = request.POST.get('invest', '500')
   type = RobotMember.objects.get(member_name=name).type #4
   stock = RobotStocks.objects.filter(type=type)
   sc = int(stock.count())
   id, mt, count,  mo = [], [], [], []
   for i in stock:
       id.append(i.stock_num)
       mt.append(i.type)
       count.append(sc)
       mo.append(money)

   #history, s, n = main(sc, id, type, count, money)
   history = {'season':'2015Q2', 'invest':'中華電(2.1%) 裕日車(17.5%) 台灣大(16.9%) 台塑化(13.2%) 震旦行(5.2%) 瑞昱(19.3%) 國泰金(1.9%) 強茂(0.5%) 康普(3.5%) 台積電(5.6%) 鴻海(14.3%) ', 'initial':'5134000.0'}
   s = ['2227', '2412', '3045', '2330', '6505', '2373', '2882', '2481', '4739', '2317']#['3045', '4726', '2227', '4915', '2373', '6281', '3702', '2481', '3548', '2317', '2832']
   n = [3, 12, 8, 2, 10, 5, 2, 2, 4, 8]#[1, 8, 4, 5, 4, 11, 13, 3, 10, 10, 13]
   sum, sell_stock = 0.0, []  #賣價、 賣出的股票
   m = int(RobotTransactionInfo.objects.get(stock_id='2412', date='20150401').the_close)*12000 + int(RobotTransactionInfo.objects.get(stock_id='3045', date='20150401').the_close)*8000+ int(RobotTransactionInfo.objects.get(stock_id='2330', date='20150401').the_close)*2000 + int(RobotTransactionInfo.objects.get(stock_id='6505', date='20150401').the_close)*5000\
       + int(RobotTransactionInfo.objects.get(stock_id='2373', date='20150401').the_close)*10000 + int(RobotTransactionInfo.objects.get(stock_id='2882', date='20150401').the_close)*2000 + int(RobotTransactionInfo.objects.get(stock_id='2227', date='20150401').the_close)*3000 + int(RobotTransactionInfo.objects.get(stock_id='2481', date='20150401').the_close)*2000 \
       + int(RobotTransactionInfo.objects.get(stock_id='4739', date='20150401').the_close)*4000 + int(RobotTransactionInfo.objects.get(stock_id='2317', date='20150401').the_close)*8000
   print(m)
   #for i in history:
        #Fund_set_history.objects.create(season=i['season'], invest=i['invest'], initial=i['initial'])
   for i, num in zip(s, n):
       name2 = RobotInformation.objects.get(stock_id=i).co_name
       pe_for_four_season = RobotPe.objects.get(date='2015Q2', stock_id=i).pe_for_four_season #2015Q1
       if pe_for_four_season == '--':
           pe_for_four_season = 0.0
       else:
           pe_for_four_season = float(pe_for_four_season) #201404
       evl = float(RobotCashFlowsQ.objects.get(date='201502', stock_id=i).free_cash_flows)*0.45 + pe_for_four_season*0.55
       '''if PE.objects.get(date='2015Q2', stock_id=i).coporate_estimated == '--' or Income_Statement_Q.objects.get(date='201502', stock_id=i).eps == '--':
           evl = (float(Transaction_info.objects.get(date='20150401', stock_id=i).the_close)+float(Transaction_info.objects.get(date='20150402', stock_id=i).the_close)+float(Transaction_info.objects.get(date='20150407', stock_id=i).the_close))/3.0
       else:
           evl = float(PE.objects.get(date='2015Q2', stock_id=i).coporate_estimated)*float(Income_Statement_Q.objects.get(date='201502', stock_id=i).eps) #本月(季)本益比*下月(季)每股盈餘
       '''
       dates = RobotTransactionInfo.objects.filter(date__startswith='201504', stock_id=i).order_by('date')
       count = dates.count()
       price_plus, price_minus = [], []
       for j in range(0, count):
          p = float(dates[j].the_close) #該股票在該月的股價
          price_plus.append(p)
          '''if p >= 0:
            price_plus.append(p)
          else:
            price_minus.append(p)'''
       #price_minus.reverse()
       price_plus.reverse()
       #for j in Transaction_info.objects.filter(date__startswith='201504', stock_id=i).order_by('date'): #201501
       for j in range(0, count): #201501
           #evl2 = (float(dates[j].the_close) + float(dates[j+1].the_close) + float(dates[j+2].the_close)+ float(dates[j+3].the_close)+ float(dates[j+4].the_close))/5.0
           #evl2 = (float(dates[j+3].the_close) + float(dates[j+4].the_close) + float(dates[j+5].the_close))/3.0
           buy_price = float(RobotTransactionInfo.objects.filter(date__startswith='201504', stock_id=i).order_by('date')[0].the_close)
           '''if dates[j].the_close > evl:
               net = float(dates[j].the_close)-evl
               net = round(net, ndigits=2)
               net = net*1000*num
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               trade_2015.objects.create(date=dates[j].date, sell_stock=name2, sell_price=dates[j].the_close, stocks=num, net=net)
               break'''
           if dates[j].the_close == price_plus[0] or dates[j].the_close == price_plus[1] or dates[j].the_close == price_plus[2] or dates[j].the_close == price_plus[3]: #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               #print(evl)
               print('current=' + str(dates[j].the_close))
               print('buy=' + str(buy_price))
               break

           if dates[j].the_close > buy_price*1.5 :#and dates[j].the_close > (evl2*1.5): #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               print('evl=' + str(evl))
               print('current=' + str(dates[j].the_close))
               print('buy=' + str(buy_price))
               break
           elif dates[j].the_close > buy_price*1.2 :#and dates[j].the_close > (evl2*1.2): #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               print(evl)
               print(dates[j].the_close)
               break
           '''elif dates[j].the_close > buy_price : #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               trade_2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               print(evl)
               print(dates[j].the_close)
               break'''

   for i in s:
       name2 = RobotInformation.objects.get(stock_id=i).co_name
       if i not in sell_stock:
           price = RobotTransactionInfo.objects.filter(date__startswith='201504', stock_id=i).order_by('date').last()
           date = price.date
           price = float(price.the_close)
           z = n[s.index(i)]
           net = price - float(RobotTransactionInfo.objects.filter(date__startswith='201504', stock_id=i).order_by('date').first().the_close)
           net = round(net, ndigits=2)
           net = int(net*1000*z)
           sell_stock.append(i)
           sum = sum + price*1000*z
           RobotTrade2015.objects.create(date=date, sell_stock=i+' '+name2, sell_price=price, stocks=z, net=net)
   #報酬率
   r = float((sum - m)/m)#float((sum - int(money) * 10000)/(int(money) * 10000))
   r = round(r, ndigits=2)
   RobotReturn.objects.create(re=r)
   print('sum = '+ str(sum))
   print('r = '+ str(r))

   sum, sell_stock = 0.0, []
   for i, num in zip(s, n):
       name2 = RobotInformation.objects.get(stock_id=i).co_name
       pe_for_four_season = RobotPe.objects.get(date='2015Q2', stock_id=i).pe_for_four_season
       if pe_for_four_season == '--':
           pe_for_four_season = 0.0
       else:
           pe_for_four_season = float(pe_for_four_season)
       evl = float(RobotCashFlowsQ.objects.get(date='201502', stock_id=i).free_cash_flows)*0.45 + pe_for_four_season*0.55
       '''if PE.objects.get(date='2015Q2', stock_id=i).coporate_estimated == '--' or Income_Statement_Q.objects.get(date='201502', stock_id=i).eps == '--':
           evl = (float(Transaction_info.objects.get(date='20150401', stock_id=i).the_close)+float(Transaction_info.objects.get(date='20150402', stock_id=i).the_close)+float(Transaction_info.objects.get(date='20150407', stock_id=i).the_close))/3.0
       else:
           evl = float(PE.objects.get(date='2015Q2', stock_id=i).coporate_estimated)*float(Income_Statement_Q.objects.get(date='201502', stock_id=i).eps) #本月(季)本益比*下月(季)每股盈餘
       '''
       dates = RobotTransactionInfo.objects.filter(date__startswith='201505', stock_id=i).order_by('date')
       count = dates.count()
       price_plus, price_minus = [], []
       for j in range(0, count):
          p = float(dates[j].the_close) #該股票在該月的股價
          price_plus.append(p)
          '''if p >= 0:
            price_plus.append(p)
          else:
            price_minus.append(p)'''
       #price_minus.reverse()
       price_plus.reverse()
       #for j in Transaction_info.objects.filter(date__startswith='201504', stock_id=i).order_by('date'): #201501
       for j in range(0, count): #201501
           #evl = (float(dates[j].the_close) + float(dates[j+1].the_close) + float(dates[j+2].the_close)+ float(dates[j+3].the_close)+ float(dates[j+4].the_close))/5.0
           #evl2 = (float(dates[j+3].the_close) + float(dates[j+4].the_close) + float(dates[j+5].the_close))/3.0
           buy_price = float(RobotTransactionInfo.objects.filter(date__startswith='201505', stock_id=i).order_by('date')[0].the_close)
           '''if dates[j].the_close > evl:
               net = float(dates[j].the_close)-evl
               net = round(net, ndigits=2)
               net = net*1000*num
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               trade_2015.objects.create(date=dates[j].date, sell_stock=name2, sell_price=dates[j].the_close, stocks=num, net=net)
               break'''
           if dates[j].the_close == price_plus[0] or dates[j].the_close == price_plus[1] : #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               #print(evl)
               print('current=' + str(dates[j].the_close))
               print('buy=' + str(buy_price))
               break
           if dates[j].the_close > buy_price*1.5 : #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               print('evl=' + str(evl))
               print('current=' + str(dates[j].the_close))
               print('buy=' + str(buy_price))
               break
           elif dates[j].the_close > buy_price*1.2 : #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               print(evl)
               print(dates[j].the_close)
               break
       '''for j in Transaction_info.objects.filter(date__startswith='201505', stock_id=i).order_by('date'):
           if j.the_close > (evl*2): #if j.the_close > (evl*1.5):
               net = float(j.the_close)-float(Transaction_info.objects.filter(date__startswith='201505', stock_id=i).order_by('date')[0].the_close)
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(j.the_close)*1000*num
               trade_2015.objects.create(date=j.date, sell_stock=i+' '+name2, sell_price=j.the_close, stocks=num, net=net)
               print(evl)
               print(j.the_close)
               break'''
   for i in s:
       name2 = RobotInformation.objects.get(stock_id=i).co_name
       if i not in sell_stock:
           price = RobotTransactionInfo.objects.filter(date__startswith='201505', stock_id=i).order_by('date').last()
           date = price.date
           price = float(price.the_close)
           z = n[s.index(i)]
           net = price - float(RobotTransactionInfo.objects.filter(date__startswith='201505', stock_id=i).order_by('date').first().the_close)
           net = round(net, ndigits=2)
           net = int(net*1000*z)
           sell_stock.append(i)
           sum = sum + price*1000*z
           RobotTrade2015.objects.create(date=date, sell_stock=i+' '+name2, sell_price=price, stocks=z, net=net)
   r = float((sum - m)/m)#float((sum - int(money) * 10000)/(int(money) * 10000))
   r = round(r, ndigits=2)
   RobotReturn.objects.create(re=r)
   print('sum = '+ str(sum))
   print('r = '+ str(r))

   '''if r > xx:
       money = xx
   mo = []
   for i in stock:
       mo.append(money)
   history, s, n = main(sc, id, type, count, money)'''
   sum, sell_stock = 0.0, []
   for i, num in zip(s, n):
       name2 = RobotInformation.objects.get(stock_id=i).co_name
       pe_for_four_season = RobotPe.objects.get(date='2015Q1', stock_id=i).pe_for_four_season
       if pe_for_four_season == '--':
           pe_for_four_season = 0.0
       else:
           pe_for_four_season = float(pe_for_four_season)
       evl = float(RobotCashFlowsQ.objects.get(date='201502', stock_id=i).free_cash_flows)*0.45 + pe_for_four_season*0.55
       '''if PE.objects.get(date='2015Q2', stock_id=i).coporate_estimated == '--' or Income_Statement_Q.objects.get(date='201502', stock_id=i).eps == '--':
           evl = (float(Transaction_info.objects.get(date='20150401', stock_id=i).the_close)+float(Transaction_info.objects.get(date='20150402', stock_id=i).the_close)+float(Transaction_info.objects.get(date='20150407', stock_id=i).the_close))/3.0
       else:
           evl = float(PE.objects.get(date='2015Q2', stock_id=i).coporate_estimated)*float(Income_Statement_Q.objects.get(date='201502', stock_id=i).eps) #本月(季)本益比*下月(季)每股盈餘
       '''
       dates = RobotTransactionInfo.objects.filter(date__startswith='201506', stock_id=i).order_by('date')
       count = dates.count()
       price_plus, price_minus = [], []
       for j in range(0, count):
          p = float(dates[j].the_close) #該股票在該月的股價
          price_plus.append(p)
          '''if p >= 0:
            price_plus.append(p)
          else:
            price_minus.append(p)'''
       #price_minus.reverse()
       price_plus.reverse()
       #for j in Transaction_info.objects.filter(date__startswith='201504', stock_id=i).order_by('date'): #201501
       for j in range(0, count): #201501
           #evl = (float(dates[j].the_close) + float(dates[j+1].the_close) + float(dates[j+2].the_close)+ float(dates[j+3].the_close)+ float(dates[j+4].the_close))/5.0
           #evl2 = (float(dates[j+3].the_close) + float(dates[j+4].the_close) + float(dates[j+5].the_close))/3.0
           buy_price = float(RobotTransactionInfo.objects.filter(date__startswith='201506', stock_id=i).order_by('date')[0].the_close)
           '''if dates[j].the_close > evl:
               net = float(dates[j].the_close)-evl
               net = round(net, ndigits=2)
               net = net*1000*num
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               trade_2015.objects.create(date=dates[j].date, sell_stock=name2, sell_price=dates[j].the_close, stocks=num, net=net)
               break'''
           if dates[j].the_close == price_plus[0] or dates[j].the_close == price_plus[1]: #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               #print(evl)
               print('current=' + str(dates[j].the_close))
               print('buy=' + str(buy_price))
               break
           if dates[j].the_close > buy_price*1.5 : #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               print('evl=' + str(evl))
               print('current=' + str(dates[j].the_close))
               print('buy=' + str(buy_price))
               break
           elif dates[j].the_close > buy_price*1.2 : #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               print(evl)
               print(dates[j].the_close)
               break
   for i in s:
       name2 = RobotInformation.objects.get(stock_id=i).co_name
       if i not in sell_stock:
           price = RobotTransactionInfo.objects.filter(date__startswith='201506', stock_id=i).order_by('date').last()
           date = price.date
           price = float(price.the_close)
           z = n[s.index(i)]
           net = price - float(RobotTransactionInfo.objects.filter(date__startswith='201506', stock_id=i).order_by('date').first().the_close)
           net = round(net, ndigits=2)
           net = int(net*1000*z)
           sell_stock.append(i)
           sum = sum + price*1000*z
           RobotTrade2015.objects.create(date=date, sell_stock=i+' '+name2, sell_price=price, stocks=z, net=net)
   r = float((sum - m)/m)#float((sum - int(money) * 10000)/(int(money) * 10000))
   r = round(r, ndigits=2)
   RobotReturn.objects.create(re=r)
   print('sum = '+ str(sum))
   print('r = '+ str(r))
   return HttpResponse()


# 原版
def fund0(request):
   name = ''
   loginstatus = False
   try:
        name = request.session['name']
        loginstatus = True
   except:
        return HttpResponseRedirect('/login/?back=資金管理')

   money = request.POST.get('invest', '500')
   type = RobotMember.objects.get(member_name=name).type #4
   stock = RobotStocks.objects.filter(type=type)
   sc = int(stock.count())
   id, mt, count,  mo= [], [], [], []
   for i in stock:
       id.append(i.stock_num)
       mt.append(i.type)
       count.append(sc)
       mo.append(money)

   #history, s, n = main(sc, id, type, count, money)
   history = {'season':'2015Q2', 'invest':'台灣大(2.1%) 永昕(8.9%) 裕日車(26.2%) 致伸(3.9%) 震旦行(4.3%) 全國電(13.5%) 大聯大(9.5%) 強茂(0.9%) 兆利(7.6%) 鴻海(17.4%) 台產(5.8%) ', 'initial':'5021200.0'}
   s = ['2412', '3045', '2330', '6505', '2373', '2379', '2882', '2481', '4739', '2317']
   n = [14, 8, 2, 15, 12, 6, 2, 2, 4, 10]
   sum, sell_stock = 0.0, []  #賣價、 賣出的股票
   #for i in history:
        #Fund_set_history.objects.create(season=i['season'], invest=i['invest'], initial=i['initial'])
   for i, num in zip(s, n):
       name2 = RobotInformation.objects.get(stock_id=i).co_name
       pe_for_four_season = RobotPe.objects.get(date='2015Q2', stock_id=i).pe_for_four_season #2015Q1
       if pe_for_four_season == '--':
           pe_for_four_season = 0.0
       else:
           pe_for_four_season = float(pe_for_four_season) #201404
       #evl = float(Cash_Flows_Q.objects.get(date='201501', stock_id=i).free_cash_flows)*0.45 + pe_for_four_season*0.55
       '''if PE.objects.get(date='2015Q2', stock_id=i).coporate_estimated == '--' or Income_Statement_Q.objects.get(date='201502', stock_id=i).eps == '--':
           evl = (float(Transaction_info.objects.get(date='20150401', stock_id=i).the_close)+float(Transaction_info.objects.get(date='20150402', stock_id=i).the_close)+float(Transaction_info.objects.get(date='20150407', stock_id=i).the_close))/3.0
       else:
           evl = float(PE.objects.get(date='2015Q2', stock_id=i).coporate_estimated)*float(Income_Statement_Q.objects.get(date='201502', stock_id=i).eps) #本月(季)本益比*下月(季)每股盈餘
       '''
       dates = RobotTransactionInfo.objects.filter(date__startswith='201504', stock_id=i).order_by('date')
       count = dates.count()
       #for j in Transaction_info.objects.filter(date__startswith='201504', stock_id=i).order_by('date'): #201501
       for j in range(0, count): #201501
           #evl = (float(dates[j].the_close) + float(dates[j+1].the_close) + float(dates[j+2].the_close)+ float(dates[j+3].the_close)+ float(dates[j+4].the_close))/5.0
           #evl2 = (float(dates[j+3].the_close) + float(dates[j+4].the_close) + float(dates[j+5].the_close))/3.0
           buy_price = float(RobotTransactionInfo.objects.filter(date__startswith='201504', stock_id=i).order_by('date')[0].the_close)
           if dates[j].the_close > buy_price*1.5 : #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               #print(evl)
               print(dates[j].the_close)
               break
           '''elif dates[j].the_close > buy_price*1.2 and evl > buy_price: #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               trade_2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               print(evl)
               print(dates[j].the_close)
               break
           elif dates[j].the_close > buy_price : #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               trade_2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               print(evl)
               print(dates[j].the_close)
               break'''
   for i in s:
       name2 = RobotInformation.objects.get(stock_id=i).co_name
       if i not in sell_stock:
           price = RobotTransactionInfo.objects.filter(date__startswith='201504', stock_id=i).order_by('date').last()
           date = price.date
           price = float(price.the_close)
           z = n[s.index(i)]
           net = price - float(RobotTransactionInfo.objects.filter(date__startswith='201504', stock_id=i).order_by('date').first().the_close)
           net = round(net, ndigits=2)
           net = int(net*1000*z)
           sell_stock.append(i)
           sum = sum + price*1000*z
           RobotTrade2015.objects.create(date=date, sell_stock=i+' '+name2, sell_price=price, stocks=z, net=net)
   #報酬率
   #r = float((sum - int(money) * 10000)/(int(money) * 10000))
   r = float((sum - 5860600)/5860600)
   r = round(r, ndigits=2)
   RobotReturn.objects.create(re=r)
   print('sum = '+ str(sum))
   print('r = '+ str(r))

   sum, sell_stock = 0.0, []
   for i, num in zip(s, n):
       name2 = RobotInformation.objects.get(stock_id=i).co_name
       pe_for_four_season = RobotPe.objects.get(date='2015Q2', stock_id=i).pe_for_four_season
       if pe_for_four_season == '--':
           pe_for_four_season = 0.0
       else:
           pe_for_four_season = float(pe_for_four_season)
       evl = float(RobotCashFlowsQ.objects.get(date='201502', stock_id=i).free_cash_flows)*0.45 + pe_for_four_season*0.55
       '''if PE.objects.get(date='2015Q2', stock_id=i).coporate_estimated == '--' or Income_Statement_Q.objects.get(date='201502', stock_id=i).eps == '--':
           evl = (float(Transaction_info.objects.get(date='20150401', stock_id=i).the_close)+float(Transaction_info.objects.get(date='20150402', stock_id=i).the_close)+float(Transaction_info.objects.get(date='20150407', stock_id=i).the_close))/3.0
       else:
           evl = float(PE.objects.get(date='2015Q2', stock_id=i).coporate_estimated)*float(Income_Statement_Q.objects.get(date='201502', stock_id=i).eps) #本月(季)本益比*下月(季)每股盈餘
       '''
       for j in RobotTransactionInfo.objects.filter(date__startswith='201505', stock_id=i).order_by('date'):
           if j.the_close > (evl*2): #if j.the_close > (evl*1.5):
               net = float(j.the_close)-float(RobotTransactionInfo.objects.filter(date__startswith='201505', stock_id=i).order_by('date')[0].the_close)
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(j.the_close)*1000*num
               RobotTrade2015.objects.create(date=j.date, sell_stock=i+' '+name2, sell_price=j.the_close, stocks=num, net=net)
               print(evl)
               print(j.the_close)
               break
   for i in s:
       name2 = RobotInformation.objects.get(stock_id=i).co_name
       if i not in sell_stock:
           price = RobotTransactionInfo.objects.filter(date__startswith='201505', stock_id=i).order_by('date').last()
           date = price.date
           price = float(price.the_close)
           z = n[s.index(i)]
           net = price - float(RobotTransactionInfo.objects.filter(date__startswith='201505', stock_id=i).order_by('date').first().the_close)
           net = round(net, ndigits=2)
           net = int(net*1000*z)
           sell_stock.append(i)
           sum = sum + price*1000*z
           RobotTrade2015.objects.create(date=date, sell_stock=i+' '+name2, sell_price=price, stocks=z, net=net)
   #r = float((sum - int(money) * 10000)/(int(money) * 10000))
   r = float((sum - 5860600)/5860600)
   r = round(r, ndigits=2)
   RobotReturn.objects.create(re=r)
   '''if r > xx:
       money = xx
   mo = []
   for i in stock:
       mo.append(money)
   history, s, n = main(sc, id, type, count, money)'''
   sum, sell_stock = 0.0, []
   for i, num in zip(s, n):
       name2 = RobotInformation.objects.get(stock_id=i).co_name
       pe_for_four_season = RobotPe.objects.get(date='2015Q1', stock_id=i).pe_for_four_season
       if pe_for_four_season == '--':
           pe_for_four_season = 0.0
       else:
           pe_for_four_season = float(pe_for_four_season)
       evl = float(RobotCashFlowsQ.objects.get(date='201501', stock_id=i).free_cash_flows)*0.45 + pe_for_four_season*0.55
       '''if PE.objects.get(date='2015Q2', stock_id=i).coporate_estimated == '--' or Income_Statement_Q.objects.get(date='201502', stock_id=i).eps == '--':
           evl = (float(Transaction_info.objects.get(date='20150401', stock_id=i).the_close)+float(Transaction_info.objects.get(date='20150402', stock_id=i).the_close)+float(Transaction_info.objects.get(date='20150407', stock_id=i).the_close))/3.0
       else:
           evl = float(PE.objects.get(date='2015Q2', stock_id=i).coporate_estimated)*float(Income_Statement_Q.objects.get(date='201502', stock_id=i).eps) #本月(季)本益比*下月(季)每股盈餘
       '''
       for j in RobotTransactionInfo.objects.filter(date__startswith='201506', stock_id=i).order_by('date'):
           if j.the_close > (evl*2): #if j.the_close > (evl*1.5):
               net = float(j.the_close)-float(RobotTransactionInfo.objects.filter(date__startswith='201506', stock_id=i).order_by('date')[0].the_close)
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(j.the_close)*1000*num
               RobotTrade2015.objects.create(date=j.date, sell_stock=i+' '+name2, sell_price=j.the_close, stocks=num, net=net)
               print(evl)
               print(j.the_close)
               break
   for i in s:
       name2 = RobotInformation.objects.get(stock_id=i).co_name
       if i not in sell_stock:
           price = RobotTransactionInfo.objects.filter(date__startswith='201506', stock_id=i).order_by('date').last()
           date = price.date
           price = float(price.the_close)
           z = n[s.index(i)]
           net = price - float(RobotTransactionInfo.objects.filter(date__startswith='201506', stock_id=i).order_by('date').first().the_close)
           net = round(net, ndigits=2)
           net = int(net*1000*z)
           sell_stock.append(i)
           sum = sum + price*1000*z
           RobotTrade2015.objects.create(date=date, sell_stock=i+' '+name2, sell_price=price, stocks=z, net=net)
   #r = float((sum - int(money) * 10000)/(int(money) * 10000))
   r = float((sum - 5860600)/5860600)
   r = round(r, ndigits=2)
   RobotReturn.objects.create(re=r)
   return HttpResponse()


# 原版第一季(?) main2(sc, id, mt, count, mo)
def fund1(request):
   name = ''
   loginstatus = False
   try:
        name = request.session['name']
        loginstatus = True
   except:
        return HttpResponseRedirect('/login/?back=資金管理')

   money = request.POST.get('invest', '500')
   type = RobotMember.objects.get(member_name=name).type #4
   stock = RobotStocks.objects.filter(type=type)
   sc = int(stock.count())
   id, mt, count,  mo= [], [], [], []
   for i in stock:
       id.append(i.stock_num)
       mt.append(i.type)
       count.append(sc)
       mo.append(money)

   #history, s, n = main(sc, id, type, count, money)
   history = {'season':'2015Q2', 'invest':'台灣大(2.1%) 永昕(8.9%) 裕日車(26.2%) 致伸(3.9%) 震旦行(4.3%) 全國電(13.5%) 大聯大(9.5%) 強茂(0.9%) 兆利(7.6%) 鴻海(17.4%) 台產(5.8%) ', 'initial':'5021200.0'}
   s = ['2412', '3045', '2330', '6505', '2373', '2379', '2882', '2481', '4739', '2317']#['3045', '4726', '2227', '4915', '2373', '6281', '3702', '2481', '3548', '2317', '2832']
   n = [14, 8, 2, 15, 12, 6, 2, 2, 4, 10]#[1, 8, 4, 5, 4, 11, 13, 3, 10, 10, 13]
   sum, sell_stock = 0.0, []  #賣價、 賣出的股票
   m = int(RobotTransactionInfo.objects.get(stock_id='2412', date='20150105').the_close)*14000 + int(RobotTransactionInfo.objects.get(stock_id='3045', date='20150105').the_close)*8000+ int(RobotTransactionInfo.objects.get(stock_id='2330', date='20150105').the_close)*2000 + int(RobotTransactionInfo.objects.get(stock_id='6505', date='20150105').the_close)*15000\
       + int(RobotTransactionInfo.objects.get(stock_id='2373', date='20150105').the_close)*12000 + int(RobotTransactionInfo .objects.get(stock_id='2882', date='20150105').the_close)*6000 + int(RobotTransactionInfo.objects.get(stock_id='2882', date='20150105').the_close)*2000 + int(RobotTransactionInfo.objects.get(stock_id='2481', date='20150105').the_close)*2000 \
       + int(RobotTransactionInfo.objects.get(stock_id='4739', date='20150105').the_close)*4000 + int(RobotTransactionInfo.objects.get(stock_id='2317', date='20150105').the_close)*10000
   print('money='+str(m))
   #for i in history:
        #Fund_set_history.objects.create(season=i['season'], invest=i['invest'], initial=i['initial'])
   for i, num in zip(s, n):
       name2 = RobotInformation.objects.get(stock_id=i).co_name
       pe_for_four_season = RobotPe.objects.get(date='2015Q1', stock_id=i).pe_for_four_season #2015Q1
       if pe_for_four_season == '--':
           pe_for_four_season = 0.0
       else:
           pe_for_four_season = float(pe_for_four_season) #201404
       evl = float(RobotCashFlowsQ.objects.get(date='201501', stock_id=i).free_cash_flows)*0.45 + pe_for_four_season*0.55
       '''if PE.objects.get(date='2015Q2', stock_id=i).coporate_estimated == '--' or Income_Statement_Q.objects.get(date='201502', stock_id=i).eps == '--':
           evl = (float(Transaction_info.objects.get(date='20150401', stock_id=i).the_close)+float(Transaction_info.objects.get(date='20150402', stock_id=i).the_close)+float(Transaction_info.objects.get(date='20150407', stock_id=i).the_close))/3.0
       else:
           evl = float(PE.objects.get(date='2015Q2', stock_id=i).coporate_estimated)*float(Income_Statement_Q.objects.get(date='201502', stock_id=i).eps) #本月(季)本益比*下月(季)每股盈餘
       '''
       dates = RobotTransactionInfo.objects.filter(date__startswith='201501', stock_id=i).order_by('date')
       count = dates.count()
       price_plus, price_minus = [], []
       for j in range(0, count):
          p = float(dates[j].the_close) #該股票在該月的股價
          price_plus.append(p)
          '''if p >= 0:
            price_plus.append(p)
          else:
            price_minus.append(p)'''
       #price_minus.reverse()
       price_plus.reverse()
       #for j in Transaction_info.objects.filter(date__startswith='201504', stock_id=i).order_by('date'): #201501
       for j in range(0, count): #201501
           #evl2 = (float(dates[j].the_close) + float(dates[j+1].the_close) + float(dates[j+2].the_close)+ float(dates[j+3].the_close)+ float(dates[j+4].the_close))/5.0
           #evl2 = (float(dates[j+3].the_close) + float(dates[j+4].the_close) + float(dates[j+5].the_close))/3.0
           buy_price = float(RobotTransactionInfo.objects.filter(date__startswith='201501', stock_id=i).order_by('date')[0].the_close)
           '''if dates[j].the_close > evl:
               net = float(dates[j].the_close)-evl
               net = round(net, ndigits=2)
               net = net*1000*num
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               trade_2015.objects.create(date=dates[j].date, sell_stock=name2, sell_price=dates[j].the_close, stocks=num, net=net)
               break'''
           if dates[j].the_close == price_plus[0] or dates[j].the_close == price_plus[1] or dates[j].the_close == price_plus[2] or dates[j].the_close == price_plus[3]: #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               #print(evl)
               print('current=' + str(dates[j].the_close))
               print('buy=' + str(buy_price))
               break

           if dates[j].the_close > buy_price*1.5 :#and dates[j].the_close > (evl2*1.5): #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               print('evl=' + str(evl))
               print('current=' + str(dates[j].the_close))
               print('buy=' + str(buy_price))
               break
           elif dates[j].the_close > buy_price*1.2 :#and dates[j].the_close > (evl2*1.2): #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               print(evl)
               print(dates[j].the_close)
               break
           '''elif dates[j].the_close > buy_price : #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               trade_2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               print(evl)
               print(dates[j].the_close)
               break'''

   for i in s:
       name2 = RobotInformation.objects.get(stock_id=i).co_name
       if i not in sell_stock:
           price = RobotTransactionInfo.objects.filter(date__startswith='201501', stock_id=i).order_by('date').last()
           date = price.date
           price = float(price.the_close)
           z = n[s.index(i)]
           net = price - float(RobotTransactionInfo.objects.filter(date__startswith='201501', stock_id=i).order_by('date').first().the_close)
           net = round(net, ndigits=2)
           net = int(net*1000*z)
           sell_stock.append(i)
           sum = sum + price*1000*z
           RobotTrade2015.objects.create(date=date, sell_stock=i+' '+name2, sell_price=price, stocks=z, net=net)
   #報酬率
   r = float((sum - m)/m)#float((sum - int(money) * 10000)/(int(money) * 10000))
   r = round(r, ndigits=2)
   RobotReturn.objects.create(re=r)
   print('sum = '+ str(sum))
   print('r = '+ str(r))

   sum, sell_stock = 0.0, []
   for i, num in zip(s, n):
       name2 = RobotInformation.objects.get(stock_id=i).co_name
       pe_for_four_season = RobotPe.objects.get(date='2015Q1', stock_id=i).pe_for_four_season
       if pe_for_four_season == '--':
           pe_for_four_season = 0.0
       else:
           pe_for_four_season = float(pe_for_four_season)
       evl = float(RobotCashFlowsQ.objects.get(date='201501', stock_id=i).free_cash_flows)*0.45 + pe_for_four_season*0.55
       '''if PE.objects.get(date='2015Q2', stock_id=i).coporate_estimated == '--' or Income_Statement_Q.objects.get(date='201502', stock_id=i).eps == '--':
           evl = (float(Transaction_info.objects.get(date='20150401', stock_id=i).the_close)+float(Transaction_info.objects.get(date='20150402', stock_id=i).the_close)+float(Transaction_info.objects.get(date='20150407', stock_id=i).the_close))/3.0
       else:
           evl = float(PE.objects.get(date='2015Q2', stock_id=i).coporate_estimated)*float(Income_Statement_Q.objects.get(date='201502', stock_id=i).eps) #本月(季)本益比*下月(季)每股盈餘
       '''
       dates = RobotTransactionInfo.objects.filter(date__startswith='201502', stock_id=i).order_by('date')
       count = dates.count()
       price_plus, price_minus = [], []
       for j in range(0, count):
          p = float(dates[j].the_close) #該股票在該月的股價
          price_plus.append(p)
          '''if p >= 0:
            price_plus.append(p)
          else:
            price_minus.append(p)'''
       #price_minus.reverse()
       price_plus.reverse()
       #for j in Transaction_info.objects.filter(date__startswith='201504', stock_id=i).order_by('date'): #201501
       for j in range(0, count): #201501
           #evl = (float(dates[j].the_close) + float(dates[j+1].the_close) + float(dates[j+2].the_close)+ float(dates[j+3].the_close)+ float(dates[j+4].the_close))/5.0
           #evl2 = (float(dates[j+3].the_close) + float(dates[j+4].the_close) + float(dates[j+5].the_close))/3.0
           buy_price = float(RobotTransactionInfo.objects.filter(date__startswith='201502', stock_id=i).order_by('date')[0].the_close)
           '''if dates[j].the_close > evl:
               net = float(dates[j].the_close)-evl
               net = round(net, ndigits=2)
               net = net*1000*num
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               trade_2015.objects.create(date=dates[j].date, sell_stock=name2, sell_price=dates[j].the_close, stocks=num, net=net)
               break'''
           if dates[j].the_close == price_plus[0] or dates[j].the_close == price_plus[1] : #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               #print(evl)
               print('current=' + str(dates[j].the_close))
               print('buy=' + str(buy_price))
               break
           if dates[j].the_close > buy_price*1.5 : #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               print('evl=' + str(evl))
               print('current=' + str(dates[j].the_close))
               print('buy=' + str(buy_price))
               break
           elif dates[j].the_close > buy_price*1.2 : #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               print(evl)
               print(dates[j].the_close)
               break
       '''for j in Transaction_info.objects.filter(date__startswith='201505', stock_id=i).order_by('date'):
           if j.the_close > (evl*2): #if j.the_close > (evl*1.5):
               net = float(j.the_close)-float(Transaction_info.objects.filter(date__startswith='201505', stock_id=i).order_by('date')[0].the_close)
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(j.the_close)*1000*num
               trade_2015.objects.create(date=j.date, sell_stock=i+' '+name2, sell_price=j.the_close, stocks=num, net=net)
               print(evl)
               print(j.the_close)
               break'''
   for i in s:
       name2 = RobotInformation.objects.get(stock_id=i).co_name
       if i not in sell_stock:
           price = RobotTransactionInfo.objects.filter(date__startswith='201502', stock_id=i).order_by('date').last()
           date = price.date
           price = float(price.the_close)
           z = n[s.index(i)]
           net = price - float(RobotTransactionInfo.objects.filter(date__startswith='201502', stock_id=i).order_by('date').first().the_close)
           net = round(net, ndigits=2)
           net = int(net*1000*z)
           sell_stock.append(i)
           sum = sum + price*1000*z
           RobotTrade2015.objects.create(date=date, sell_stock=i+' '+name2, sell_price=price, stocks=z, net=net)
   r = r = float((sum - m)/m)#float((sum - int(money) * 10000)/(int(money) * 10000))
   r = round(r, ndigits=2)
   RobotReturn.objects.create(re=r)
   print('sum = '+ str(sum))
   print('r = '+ str(r))

   '''if r > xx:
       money = xx
   mo = []
   for i in stock:
       mo.append(money)
   history, s, n = main(sc, id, type, count, money)'''
   sum, sell_stock = 0.0, []
   for i, num in zip(s, n):
       name2 = RobotInformation.objects.get(stock_id=i).co_name
       pe_for_four_season = RobotPe.objects.get(date='2015Q1', stock_id=i).pe_for_four_season
       if pe_for_four_season == '--':
           pe_for_four_season = 0.0
       else:
           pe_for_four_season = float(pe_for_four_season)
       evl = float(RobotCashFlowsQ.objects.get(date='201502', stock_id=i).free_cash_flows)*0.45 + pe_for_four_season*0.55
       '''if PE.objects.get(date='2015Q2', stock_id=i).coporate_estimated == '--' or Income_Statement_Q.objects.get(date='201502', stock_id=i).eps == '--':
           evl = (float(Transaction_info.objects.get(date='20150401', stock_id=i).the_close)+float(Transaction_info.objects.get(date='20150402', stock_id=i).the_close)+float(Transaction_info.objects.get(date='20150407', stock_id=i).the_close))/3.0
       else:
           evl = float(PE.objects.get(date='2015Q2', stock_id=i).coporate_estimated)*float(Income_Statement_Q.objects.get(date='201502', stock_id=i).eps) #本月(季)本益比*下月(季)每股盈餘
       '''
       dates = RobotTransactionInfo.objects.filter(date__startswith='201503', stock_id=i).order_by('date')
       count = dates.count()
       price_plus, price_minus = [], []
       for j in range(0, count):
          p = float(dates[j].the_close) #該股票在該月的股價
          price_plus.append(p)
          '''if p >= 0:
            price_plus.append(p)
          else:
            price_minus.append(p)'''
       #price_minus.reverse()
       price_plus.reverse()
       #for j in Transaction_info.objects.filter(date__startswith='201504', stock_id=i).order_by('date'): #201501
       for j in range(0, count): #201501
           #evl = (float(dates[j].the_close) + float(dates[j+1].the_close) + float(dates[j+2].the_close)+ float(dates[j+3].the_close)+ float(dates[j+4].the_close))/5.0
           #evl2 = (float(dates[j+3].the_close) + float(dates[j+4].the_close) + float(dates[j+5].the_close))/3.0
           buy_price = float(RobotTransactionInfo.objects.filter(date__startswith='201503', stock_id=i).order_by('date')[0].the_close)
           '''if dates[j].the_close > evl:
               net = float(dates[j].the_close)-evl
               net = round(net, ndigits=2)
               net = net*1000*num
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               trade_2015.objects.create(date=dates[j].date, sell_stock=name2, sell_price=dates[j].the_close, stocks=num, net=net)
               break'''
           if dates[j].the_close == price_plus[0] or dates[j].the_close == price_plus[1]: #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               #print(evl)
               print('current=' + str(dates[j].the_close))
               print('buy=' + str(buy_price))
               break
           if dates[j].the_close > buy_price*1.5 : #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               print('evl=' + str(evl))
               print('current=' + str(dates[j].the_close))
               print('buy=' + str(buy_price))
               break
           elif dates[j].the_close > buy_price*1.2 : #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               print(evl)
               print(dates[j].the_close)
               break
   for i in s:
       name2 = RobotInformation.objects.get(stock_id=i).co_name
       if i not in sell_stock:
           price = RobotTransactionInfo.objects.filter(date__startswith='201503', stock_id=i).order_by('date').last()
           date = price.date
           price = float(price.the_close)
           z = n[s.index(i)]
           net = price - float(RobotTransactionInfo.objects.filter(date__startswith='201503', stock_id=i).order_by('date').first().the_close)
           net = round(net, ndigits=2)
           net = int(net*1000*z)
           sell_stock.append(i)
           sum = sum + price*1000*z
           RobotTrade2015.objects.create(date=date, sell_stock=i+' '+name2, sell_price=price, stocks=z, net=net)
   r = float((sum - m)/m)#float((sum - int(money) * 10000)/(int(money) * 10000))
   r = round(r, ndigits=2)
   RobotReturn.objects.create(re=r)
   print('sum = '+ str(sum))
   print('r = '+ str(r))
   return HttpResponse()


# 第三季
def fund3(request): # 第三季
   name = ''
   loginstatus = False
   try:
        name = request.session['name']
        loginstatus = True
   except:
        return HttpResponseRedirect('/login/?back=資金管理')

   money = request.POST.get('invest', '500')
   type = RobotMember.objects.get(member_name=name).type #4
   stock = RobotStocks.objects.filter(type=type)
   sc = int(stock.count())
   id, mt, count,  mo= [], [], [], []
   for i in stock:
       id.append(i.stock_num)
       mt.append(i.type)
       count.append(sc)
       mo.append(money)
   #報酬率: 0.08、0.03、0.0
   #history, s, n, m= main(sc, id, type, count, money)
   history = {'season':'2015Q3', 'invest':'台積電(4.8%) 鴻海(26.3%) 台塑(18.7%) 中華電(18.6%) 富邦(5.3%) 台灣大(3.6%) 遠傳(6.5%) 震旦行(3.5%) 台塑(11.4%) 強茂(2.2%) 兆利(5.8%) ', 'initial':'5562500'}
   s = ['2330', '2317', '6505', '2412', '2881', '3045', '4904', '2373', '1301', '2481', '3548']
   n = [2, 12, 15, 11, 5, 2, 5, 4, 9, 11, 15]#[1, 8, 4, 5, 4, 11, 13, 3, 10, 10, 13]
   sum, sell_stock = 0.0, []  #賣價、 賣出的股票
   m = int(RobotTransactionInfo.objects.get(stock_id='2330', date='20150701').the_close)*2000 + int(RobotTransactionInfo.objects.get(stock_id='2317', date='20150701').the_close)*12000 + int(RobotTransactionInfo.objects.get(stock_id='6505', date='20150701').the_close)*15000 + int(RobotTransactionInfo.objects.get(stock_id='2412', date='20150701').the_close)*11000\
       + int(RobotTransactionInfo.objects.get(stock_id='2881', date='20150701').the_close)*2000 + int(RobotTransactionInfo.objects.get(stock_id='3045', date='20150701').the_close)*2000 + int(RobotTransactionInfo.objects.get(stock_id='4904', date='20150701').the_close)*5000 + int(RobotTransactionInfo.objects.get(stock_id='2373', date='20150701').the_close)*4000 \
       + int(RobotTransactionInfo.objects.get(stock_id='1301', date='20150701').the_close)*9000 + int(RobotTransactionInfo.objects.get(stock_id='2481', date='20150701').the_close)*11000 + int(RobotTransactionInfo.objects.get(stock_id='3548', date='20150701').the_close)*15000

   m = 5562500.0 #5756000
   print('money='+str(m))
   for i in history:
        RobotFundSetHistory.objects.create(season=i['season'], invest=i['invest'], initial=i['initial'])
   for i, num in zip(s, n):
       name2 = RobotInformation.objects.get(stock_id=i).co_name
       pe_for_four_season = RobotPe.objects.get(date='2015Q3', stock_id=i).pe_for_four_season #2015Q1
       if pe_for_four_season == '--':
           pe_for_four_season = 0.0
       else:
           pe_for_four_season = float(pe_for_four_season) #201404
       #evl = float(Cash_Flows_Q.objects.get(date='201503', stock_id=i).free_cash_flows)*0.45 + pe_for_four_season*0.55
       '''if PE.objects.get(date='2015Q2', stock_id=i).coporate_estimated == '--' or Income_Statement_Q.objects.get(date='201502', stock_id=i).eps == '--':
           evl = (float(Transaction_info.objects.get(date='20150401', stock_id=i).the_close)+float(Transaction_info.objects.get(date='20150402', stock_id=i).the_close)+float(Transaction_info.objects.get(date='20150407', stock_id=i).the_close))/3.0
       else:
           evl = float(PE.objects.get(date='2015Q2', stock_id=i).coporate_estimated)*float(Income_Statement_Q.objects.get(date='201502', stock_id=i).eps) #本月(季)本益比*下月(季)每股盈餘
       '''
       dates = RobotTransactionInfo.objects.filter(date__startswith='201507', stock_id=i).order_by('date')
       count = dates.count()
       price_plus, price_minus = [], []
       for j in range(0, count):
          p = float(dates[j].the_close) #該股票在該月的股價
          price_plus.append(p)
          '''if p >= 0:
            price_plus.append(p)
          else:
            price_minus.append(p)'''
       #price_minus.reverse()
       price_plus.reverse()
       #for j in Transaction_info.objects.filter(date__startswith='201504', stock_id=i).order_by('date'): #201501
       for j in range(0, count): #201501
           evl = (float(dates[j].the_close) + float(dates[j+1].the_close) + float(dates[j+2].the_close)+ float(dates[j+3].the_close)+ float(dates[j+4].the_close))/5.0
           #evl2 = (float(dates[j+3].the_close) + float(dates[j+4].the_close) + float(dates[j+5].the_close))/3.0
           buy_price = float(RobotTransactionInfo.objects.filter(date__startswith='201507', stock_id=i).order_by('date')[0].the_close)
           if dates[j].the_close > evl:
               net = float(dates[j].the_close)-evl
               net = round(net, ndigits=2)
               net = net*1000*num
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=name2, sell_price=dates[j].the_close, stocks=num, net=net)
               break
           elif dates[j].the_close == price_plus[0] or dates[j].the_close == price_plus[1] or dates[j].the_close == price_plus[2] or dates[j].the_close == price_plus[3]: #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               #print(evl)
               print('current=' + str(dates[j].the_close))
               print('buy=' + str(buy_price))
               break

           elif dates[j].the_close > buy_price*1.5 :#and dates[j].the_close > (evl2*1.5): #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               print('evl=' + str(evl))
               print('current=' + str(dates[j].the_close))
               print('buy=' + str(buy_price))
               break
           elif dates[j].the_close > buy_price*1.2 :#and dates[j].the_close > (evl2*1.2): #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               print(evl)
               print(dates[j].the_close)
               break
           '''elif dates[j].the_close > buy_price : #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               trade_2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               print(evl)
               print(dates[j].the_close)
               break'''

   for i in s:
       name2 = RobotInformation.objects.get(stock_id=i).co_name
       if i not in sell_stock:
           price = RobotTransactionInfo.objects.filter(date__startswith='201507', stock_id=i).order_by('date').last()
           date = price.date
           price = float(price.the_close)
           z = n[s.index(i)]
           net = price - float(RobotTransactionInfo.objects.filter(date__startswith='201507', stock_id=i).order_by('date').first().the_close)
           net = round(net, ndigits=2)
           net = int(net*1000*z)
           sell_stock.append(i)
           sum = sum + price*1000*z
           RobotTrade2015.objects.create(date=date, sell_stock=i+' '+name2, sell_price=price, stocks=z, net=net)
   #報酬率
   r = float((sum - m)/m)#float((sum - int(money) * 10000)/(int(money) * 10000))
   r = round(r, ndigits=2)
   RobotReturn.objects.create(re=r)
   print('sum = '+ str(sum))
   print('r = '+ str(r))

   sum, sell_stock = 0.0, []
   for i, num in zip(s, n):
       name2 = RobotInformation.objects.get(stock_id=i).co_name
       pe_for_four_season = RobotPe.objects.get(date='2015Q3', stock_id=i).pe_for_four_season
       if pe_for_four_season == '--':
           pe_for_four_season = 0.0
       else:
           pe_for_four_season = float(pe_for_four_season)
       #evl = float(Cash_Flows_Q.objects.get(date='201503', stock_id=i).free_cash_flows)*0.45 + pe_for_four_season*0.55
       '''if PE.objects.get(date='2015Q2', stock_id=i).coporate_estimated == '--' or Income_Statement_Q.objects.get(date='201502', stock_id=i).eps == '--':
           evl = (float(Transaction_info.objects.get(date='20150401', stock_id=i).the_close)+float(Transaction_info.objects.get(date='20150402', stock_id=i).the_close)+float(Transaction_info.objects.get(date='20150407', stock_id=i).the_close))/3.0
       else:
           evl = float(PE.objects.get(date='2015Q2', stock_id=i).coporate_estimated)*float(Income_Statement_Q.objects.get(date='201502', stock_id=i).eps) #本月(季)本益比*下月(季)每股盈餘
       '''
       dates = RobotTransactionInfo.objects.filter(date__startswith='201508', stock_id=i).order_by('date')
       count = dates.count()
       price_plus, price_minus = [], []
       for j in range(0, count):
          p = float(dates[j].the_close) #該股票在該月的股價
          price_plus.append(p)
          '''if p >= 0:
            price_plus.append(p)
          else:
            price_minus.append(p)'''
       #price_minus.reverse()
       price_plus.reverse()
       #for j in Transaction_info.objects.filter(date__startswith='201504', stock_id=i).order_by('date'): #201501
       for j in range(0, count): #201501
           evl = (float(dates[j].the_close) + float(dates[j+1].the_close) + float(dates[j+2].the_close)+ float(dates[j+3].the_close)+ float(dates[j+4].the_close))/5.0
           #evl2 = (float(dates[j+3].the_close) + float(dates[j+4].the_close) + float(dates[j+5].the_close))/3.0
           buy_price = float(RobotTransactionInfo.objects.filter(date__startswith='201508', stock_id=i).order_by('date')[0].the_close)
           if dates[j].the_close > evl:
               net = float(dates[j].the_close)-evl
               net = round(net, ndigits=2)
               net = net*1000*num
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=name2, sell_price=dates[j].the_close, stocks=num, net=net)
               break
           elif dates[j].the_close == price_plus[0] :#or dates[j].the_close == price_plus[1] : #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               #print(evl)
               print('current=' + str(dates[j].the_close))
               print('buy=' + str(buy_price))
               break
           elif dates[j].the_close > buy_price*1.5 : #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               print('evl=' + str(evl))
               print('current=' + str(dates[j].the_close))
               print('buy=' + str(buy_price))
               break
           elif dates[j].the_close > buy_price*1.2 : #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               print(evl)
               print(dates[j].the_close)
               break
       '''for j in Transaction_info.objects.filter(date__startswith='201505', stock_id=i).order_by('date'):
           if j.the_close > (evl*2): #if j.the_close > (evl*1.5):
               net = float(j.the_close)-float(Transaction_info.objects.filter(date__startswith='201505', stock_id=i).order_by('date')[0].the_close)
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(j.the_close)*1000*num
               trade_2015.objects.create(date=j.date, sell_stock=i+' '+name2, sell_price=j.the_close, stocks=num, net=net)
               print(evl)
               print(j.the_close)
               break'''
   for i in s:
       name2 = RobotInformation.objects.get(stock_id=i).co_name
       if i not in sell_stock:
           price = RobotTransactionInfo.objects.filter(date__startswith='201508', stock_id=i).order_by('date').last()
           date = price.date
           price = float(price.the_close)
           z = n[s.index(i)]
           net = price - float(RobotTransactionInfo.objects.filter(date__startswith='201508', stock_id=i).order_by('date').first().the_close)
           net = round(net, ndigits=2)
           net = int(net*1000*z)
           sell_stock.append(i)
           sum = sum + price*1000*z
           RobotTrade2015.objects.create(date=date, sell_stock=i+' '+name2, sell_price=price, stocks=z, net=net)
   r = r = float((sum - m)/m)#float((sum - int(money) * 10000)/(int(money) * 10000))
   r = round(r, ndigits=2)
   RobotReturn.objects.create(re=r)
   print('sum = '+ str(sum))
   print('r = '+ str(r))

   '''if r > xx:
       money = xx
   mo = []
   for i in stock:
       mo.append(money)
   history, s, n = main(sc, id, type, count, money)'''
   sum, sell_stock = 0.0, []
   for i, num in zip(s, n):
       name2 = RobotInformation.objects.get(stock_id=i).co_name
       pe_for_four_season = RobotPe.objects.get(date='2015Q3', stock_id=i).pe_for_four_season
       if pe_for_four_season == '--':
           pe_for_four_season = 0.0
       else:
           pe_for_four_season = float(pe_for_four_season)
       #evl = float(Cash_Flows_Q.objects.get(date='201503', stock_id=i).free_cash_flows)*0.45 + pe_for_four_season*0.55
       '''if PE.objects.get(date='2015Q2', stock_id=i).coporate_estimated == '--' or Income_Statement_Q.objects.get(date='201502', stock_id=i).eps == '--':
           evl = (float(Transaction_info.objects.get(date='20150401', stock_id=i).the_close)+float(Transaction_info.objects.get(date='20150402', stock_id=i).the_close)+float(Transaction_info.objects.get(date='20150407', stock_id=i).the_close))/3.0
       else:
           evl = float(PE.objects.get(date='2015Q2', stock_id=i).coporate_estimated)*float(Income_Statement_Q.objects.get(date='201502', stock_id=i).eps) #本月(季)本益比*下月(季)每股盈餘
       '''
       dates = RobotTransactionInfo.objects.filter(date__startswith='201509', stock_id=i).order_by('date')
       count = dates.count()
       price_plus, price_minus = [], []
       for j in range(0, count):
          p = float(dates[j].the_close) #該股票在該月的股價
          price_plus.append(p)
          '''if p >= 0:
            price_plus.append(p)
          else:
            price_minus.append(p)'''
       #price_minus.reverse()
       price_plus.reverse()
       #for j in Transaction_info.objects.filter(date__startswith='201504', stock_id=i).order_by('date'): #201501
       for j in range(0, count): #201501
           evl = (float(dates[j].the_close) + float(dates[j+1].the_close) + float(dates[j+2].the_close)+ float(dates[j+3].the_close)+ float(dates[j+4].the_close))/5.0
           #evl2 = (float(dates[j+3].the_close) + float(dates[j+4].the_close) + float(dates[j+5].the_close))/3.0
           buy_price = float(RobotTransactionInfo.objects.filter(date__startswith='201509', stock_id=i).order_by('date')[0].the_close)
           if dates[j].the_close > evl:
               net = float(dates[j].the_close)-evl
               net = round(net, ndigits=2)
               net = net*1000*num
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=name2, sell_price=dates[j].the_close, stocks=num, net=net)
               break
           elif dates[j].the_close == price_plus[0] : #or dates[j].the_close == price_plus[1]: #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               #print(evl)
               print('current=' + str(dates[j].the_close))
               print('buy=' + str(buy_price))
               break
           elif dates[j].the_close > buy_price*1.5 : #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               print('evl=' + str(evl))
               print('current=' + str(dates[j].the_close))
               print('buy=' + str(buy_price))
               break
           elif dates[j].the_close > buy_price*1.2 : #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               print(evl)
               print(dates[j].the_close)
               break
   for i in s:
       name2 = RobotInformation.objects.get(stock_id=i).co_name
       if i not in sell_stock:
           price = RobotTransactionInfo.objects.filter(date__startswith='201509', stock_id=i).order_by('date').last()
           date = price.date
           price = float(price.the_close)
           z = n[s.index(i)]
           net = price - float(RobotTransactionInfo.objects.filter(date__startswith='201509', stock_id=i).order_by('date').first().the_close)
           net = round(net, ndigits=2)
           net = int(net*1000*z)
           sell_stock.append(i)
           sum = sum + price*1000*z
           RobotTrade2015.objects.create(date=date, sell_stock=i+' '+name2, sell_price=price, stocks=z, net=net)
   r = float((sum - m)/m)#float((sum - int(money) * 10000)/(int(money) * 10000))
   r = round(r, ndigits=2)
   RobotReturn.objects.create(re=r)
   print('sum = '+ str(sum))
   print('r = '+ str(r))
   return HttpResponse()


# 第四季
def fund4(request):
   name = ''
   loginstatus = False
   try:
        name = request.session['name']
        loginstatus = True
   except:
        return HttpResponseRedirect('/login/?back=資金管理')

   money = request.POST.get('invest', '500')
   type = RobotMember.objects.get(member_name=name).type #4
   stock = RobotStocks.objects.filter(type=type)
   sc = int(stock.count())
   id, mt, count,  mo= [], [], [], []
   for i in stock:
       id.append(i.stock_num)
       mt.append(i.type)
       count.append(sc)
       mo.append(money)
   #報酬率: 0.07、0.12、0.12
   #history, s, n, m= main(sc, id, type, count, money)
   history = {'season':'2015Q2', 'invest':'台灣大(2.1%) 永昕(8.9%) 裕日車(26.2%) 致伸(3.9%) 震旦行(4.3%) 全國電(13.5%) 大聯大(9.5%) 強茂(0.9%) 兆利(7.6%) 鴻海(17.4%) 台產(5.8%) ', 'initial':'4802000.0'}
   #{'season':'2015Q3', 'invest':'台積電(4.8%) 鴻海(26.3%) 台塑(18.7%) 中華電(18.6%) 富邦(5.3%) 台灣大(3.6%) 遠傳(6.5%) 震旦行(3.5%) 台塑(11.4%) 強茂(2.2%) 兆利(5.8%) ', 'initial':'5562500'}
   s = ['3045', '4726', '2227', '4915', '2373', '6281', '3702', '2481', '3548', '2317', '2832']#['2330', '2317', '6505', '2412', '2881', '3045', '4904', '2373', '1301', '2481', '3548']
   n = [3, 8, 5, 5, 4, 15, 13, 6, 12, 11, 13]#[2, 12, 15, 11, 5, 2, 5, 4, 9, 11, 15]#[1, 8, 4, 5, 4, 11, 13, 3, 10, 10, 13]
   sum, sell_stock = 0.0, []  #賣價、 賣出的股票
   m = int(RobotTransactionInfo.objects.get(stock_id='3045', date='20151001').the_close)*3000 + int(RobotTransactionInfo.objects.get(stock_id='4726', date='20151001').the_close)*8000+ int(RobotTransactionInfo.objects.get(stock_id='2227', date='20151001').the_close)*5000 + int(RobotTransactionInfo.objects.get(stock_id='4915', date='20151001').the_close)*5000\
       + int(RobotTransactionInfo.objects.get(stock_id='2373', date='20151001').the_close)*4000 + int(RobotTransactionInfo.objects.get(stock_id='6281', date='20151001').the_close)*15000 + int(RobotTransactionInfo.objects.get(stock_id='3702', date='20151001').the_close)*13000 + int(RobotTransactionInfo.objects.get(stock_id='2481', date='20151001').the_close)*6000 \
       + int(RobotTransactionInfo.objects.get(stock_id='2317', date='20151001').the_close)*11000 + int(RobotTransactionInfo.objects.get(stock_id='3548', date='20151001').the_close)*12000 + int(RobotTransactionInfo.objects.get(stock_id='2832', date='20151001').the_close)*13000

   #m = 5021200.0#5562500.0 #5756000
   print('money='+str(m))
   #for i in history:
        #Fund_set_history.objects.create(season=i['season'], invest=i['invest'], initial=i['initial'])
   for i, num in zip(s, n):
       name2 = RobotInformation.objects.get(stock_id=i).co_name
       pe_for_four_season = RobotPe.objects.get(date='2015Q4', stock_id=i).pe_for_four_season #2015Q1
       if pe_for_four_season == '--':
           pe_for_four_season = 0.0
       else:
           pe_for_four_season = float(pe_for_four_season) #201404
       #evl = float(Cash_Flows_Q.objects.get(date='201503', stock_id=i).free_cash_flows)*0.45 + pe_for_four_season*0.55
       '''if PE.objects.get(date='2015Q2', stock_id=i).coporate_estimated == '--' or Income_Statement_Q.objects.get(date='201502', stock_id=i).eps == '--':
           evl = (float(Transaction_info.objects.get(date='20150401', stock_id=i).the_close)+float(Transaction_info.objects.get(date='20150402', stock_id=i).the_close)+float(Transaction_info.objects.get(date='20150407', stock_id=i).the_close))/3.0
       else:
           evl = float(PE.objects.get(date='2015Q2', stock_id=i).coporate_estimated)*float(Income_Statement_Q.objects.get(date='201502', stock_id=i).eps) #本月(季)本益比*下月(季)每股盈餘
       '''
       dates = RobotTransactionInfo.objects.filter(date__startswith='201510', stock_id=i).order_by('date')
       count = dates.count()
       price_plus, price_minus = [], []
       for j in range(0, count):
          p = float(dates[j].the_close) #該股票在該月的股價
          price_plus.append(p)
          '''if p >= 0:
            price_plus.append(p)
          else:
            price_minus.append(p)'''
       #price_minus.reverse()
       price_plus.reverse()
       #for j in Transaction_info.objects.filter(date__startswith='201504', stock_id=i).order_by('date'): #201501
       for j in range(0, count): #201501
           evl = (float(dates[j].the_close) + float(dates[j+1].the_close) + float(dates[j+2].the_close)+ float(dates[j+3].the_close)+ float(dates[j+4].the_close))/5.0
           #evl2 = (float(dates[j+3].the_close) + float(dates[j+4].the_close) + float(dates[j+5].the_close))/3.0
           buy_price = float(RobotTransactionInfo.objects.filter(date__startswith='201510', stock_id=i).order_by('date')[0].the_close)
           if dates[j].the_close > evl:
               net = float(dates[j].the_close) -buy_price
               net = round(net, ndigits=2)
               net = net*1000*num
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               break
           elif dates[j].the_close == price_plus[0] or dates[j].the_close == price_plus[1] or dates[j].the_close == price_plus[2] or dates[j].the_close == price_plus[3]: #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               #print(evl)
               print('current=' + str(dates[j].the_close))
               print('buy=' + str(buy_price))
               break

           elif dates[j].the_close > buy_price*1.5 :#and dates[j].the_close > (evl2*1.5): #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               print('evl=' + str(evl))
               print('current=' + str(dates[j].the_close))
               print('buy=' + str(buy_price))
               break
           elif dates[j].the_close > buy_price*1.2 :#and dates[j].the_close > (evl2*1.2): #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               print(evl)
               print(dates[j].the_close)
               break
           '''elif dates[j].the_close > buy_price : #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               trade_2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               print(evl)
               print(dates[j].the_close)
               break'''

   for i in s:
       name2 = RobotInformation.objects.get(stock_id=i).co_name
       if i not in sell_stock:
           price = RobotTransactionInfo.objects.filter(date__startswith='201510', stock_id=i).order_by('date').last()
           date = price.date
           price = float(price.the_close)
           z = n[s.index(i)]
           net = price - float(RobotTransactionInfo.objects.filter(date__startswith='201510', stock_id=i).order_by('date').first().the_close)
           net = round(net, ndigits=2)
           net = int(net*1000*z)
           sell_stock.append(i)
           sum = sum + price*1000*z
           RobotTrade2015.objects.create(date=date, sell_stock=i+' '+name2, sell_price=price, stocks=z, net=net)
   #報酬率
   r = float((sum-m)/m)#float((sum - int(money) * 10000)/(int(money) * 10000))
   r = round(r, ndigits=2)
   RobotReturn.objects.create(re=r)
   print('sum = '+ str(sum))
   print('r = '+ str(r))

   sum, sell_stock = 0.0, []
   for i, num in zip(s, n):
       name2 = RobotInformation.objects.get(stock_id=i).co_name
       pe_for_four_season = RobotPe.objects.get(date='2015Q4', stock_id=i).pe_for_four_season
       if pe_for_four_season == '--':
           pe_for_four_season = 0.0
       else:
           pe_for_four_season = float(pe_for_four_season)
       #evl = float(Cash_Flows_Q.objects.get(date='201503', stock_id=i).free_cash_flows)*0.45 + pe_for_four_season*0.55
       '''if PE.objects.get(date='2015Q2', stock_id=i).coporate_estimated == '--' or Income_Statement_Q.objects.get(date='201502', stock_id=i).eps == '--':
           evl = (float(Transaction_info.objects.get(date='20150401', stock_id=i).the_close)+float(Transaction_info.objects.get(date='20150402', stock_id=i).the_close)+float(Transaction_info.objects.get(date='20150407', stock_id=i).the_close))/3.0
       else:
           evl = float(PE.objects.get(date='2015Q2', stock_id=i).coporate_estimated)*float(Income_Statement_Q.objects.get(date='201502', stock_id=i).eps) #本月(季)本益比*下月(季)每股盈餘
       '''
       dates = RobotTransactionInfo.objects.filter(date__startswith='201511', stock_id=i).order_by('date')
       count = dates.count()
       price_plus, price_minus = [], []
       for j in range(0, count):
          p = float(dates[j].the_close) #該股票在該月的股價
          price_plus.append(p)
          '''if p >= 0:
            price_plus.append(p)
          else:
            price_minus.append(p)'''
       #price_minus.reverse()
       price_plus.reverse()
       #for j in Transaction_info.objects.filter(date__startswith='201504', stock_id=i).order_by('date'): #201501
       for j in range(0, count): #201501
           evl = (float(dates[j].the_close) + float(dates[j+1].the_close) + float(dates[j+2].the_close)+ float(dates[j+3].the_close)+ float(dates[j+4].the_close))/5.0
           #evl2 = (float(dates[j+3].the_close) + float(dates[j+4].the_close) + float(dates[j+5].the_close))/3.0
           buy_price = float(RobotTransactionInfo.objects.filter(date__startswith='201511', stock_id=i).order_by('date')[0].the_close)
           if dates[j].the_close > evl:
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = net*1000*num
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               break
           elif dates[j].the_close == price_plus[0] :#or dates[j].the_close == price_plus[1] : #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)#-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               #print(evl)
               print('current=' + str(dates[j].the_close))
               print('buy=' + str(buy_price))
               break
           elif dates[j].the_close > buy_price*1.5 : #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               print('evl=' + str(evl))
               print('current=' + str(dates[j].the_close))
               print('buy=' + str(buy_price))
               break
           elif dates[j].the_close > buy_price*1.2 : #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               print(evl)
               print(dates[j].the_close)
               break
       '''for j in Transaction_info.objects.filter(date__startswith='201505', stock_id=i).order_by('date'):
           if j.the_close > (evl*2): #if j.the_close > (evl*1.5):
               net = float(j.the_close)-float(Transaction_info.objects.filter(date__startswith='201505', stock_id=i).order_by('date')[0].the_close)
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(j.the_close)*1000*num
               trade_2015.objects.create(date=j.date, sell_stock=i+' '+name2, sell_price=j.the_close, stocks=num, net=net)
               print(evl)
               print(j.the_close)
               break'''
   for i in s:
       name2 = RobotInformation.objects.get(stock_id=i).co_name
       if i not in sell_stock:
           price = RobotTransactionInfo.objects.filter(date__startswith='201511', stock_id=i).order_by('date').last()
           date = price.date
           price = float(price.the_close)
           z = n[s.index(i)]
           net = price - float(RobotTransactionInfo.objects.filter(date__startswith='201511', stock_id=i).order_by('date').first().the_close)
           net = round(net, ndigits=2)
           net = int(net*1000*z)
           sell_stock.append(i)
           sum = sum + price*1000*z
           RobotTrade2015.objects.create(date=date, sell_stock=i+' '+name2, sell_price=price, stocks=z, net=net)
   r = float((sum-m)/m)#float((sum - int(money) * 10000)/(int(money) * 10000))
   r = round(r, ndigits=2)
   RobotReturn.objects.create(re=r)
   print('sum = '+ str(sum))
   print('r = '+ str(r))

   '''if r > xx:
       money = xx
   mo = []
   for i in stock:
       mo.append(money)
   history, s, n = main(sc, id, type, count, money)'''
   sum, sell_stock = 0.0, []
   for i, num in zip(s, n):
       name2 = RobotInformation.objects.get(stock_id=i).co_name
       pe_for_four_season = RobotPe.objects.get(date='2015Q4', stock_id=i).pe_for_four_season
       if pe_for_four_season == '--':
           pe_for_four_season = 0.0
       else:
           pe_for_four_season = float(pe_for_four_season)
       #evl = float(Cash_Flows_Q.objects.get(date='201503', stock_id=i).free_cash_flows)*0.45 + pe_for_four_season*0.55
       '''if PE.objects.get(date='2015Q2', stock_id=i).coporate_estimated == '--' or Income_Statement_Q.objects.get(date='201502', stock_id=i).eps == '--':
           evl = (float(Transaction_info.objects.get(date='20150401', stock_id=i).the_close)+float(Transaction_info.objects.get(date='20150402', stock_id=i).the_close)+float(Transaction_info.objects.get(date='20150407', stock_id=i).the_close))/3.0
       else:
           evl = float(PE.objects.get(date='2015Q2', stock_id=i).coporate_estimated)*float(Income_Statement_Q.objects.get(date='201502', stock_id=i).eps) #本月(季)本益比*下月(季)每股盈餘
       '''
       dates = RobotTransactionInfo.objects.filter(date__startswith='201512', stock_id=i).order_by('date')
       count = dates.count()
       price_plus, price_minus = [], []
       for j in range(0, count):
          p = float(dates[j].the_close) #該股票在該月的股價
          price_plus.append(p)
          '''if p >= 0:
            price_plus.append(p)
          else:
            price_minus.append(p)'''
       #price_minus.reverse()
       price_plus.reverse()
       #for j in Transaction_info.objects.filter(date__startswith='201504', stock_id=i).order_by('date'): #201501
       for j in range(0, count): #201501
           evl = (float(dates[j].the_close) + float(dates[j+1].the_close) + float(dates[j+2].the_close)+ float(dates[j+3].the_close)+ float(dates[j+4].the_close))/5.0
           #evl2 = (float(dates[j+3].the_close) + float(dates[j+4].the_close) + float(dates[j+5].the_close))/3.0
           buy_price = float(RobotTransactionInfo.objects.filter(date__startswith='201512', stock_id=i).order_by('date')[0].the_close)
           if dates[j].the_close > evl:
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = net*1000*num
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               break
           elif dates[j].the_close == price_plus[0] : #or dates[j].the_close == price_plus[1]: #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               #print(evl)
               print('current=' + str(dates[j].the_close))
               print('buy=' + str(buy_price))
               break
           elif dates[j].the_close > buy_price*1.5 : #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               print('evl=' + str(evl))
               print('current=' + str(dates[j].the_close))
               print('buy=' + str(buy_price))
               break
           elif dates[j].the_close > buy_price*1.2 : #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               print(evl)
               print(dates[j].the_close)
               break
   for i in s:
       name2 = RobotInformation.objects.get(stock_id=i).co_name
       if i not in sell_stock:
           price = RobotTransactionInfo.objects.filter(date__startswith='201512', stock_id=i).order_by('date').last()
           date = price.date
           price = float(price.the_close)
           z = n[s.index(i)]
           net = price - float(RobotTransactionInfo.objects.filter(date__startswith='201512', stock_id=i).order_by('date').first().the_close)
           net = round(net, ndigits=2)
           net = int(net*1000*z)
           sell_stock.append(i)
           sum = sum + price*1000*z
           RobotTrade2015.objects.create(date=date, sell_stock=i+' '+name2, sell_price=price, stocks=z, net=net)
   r = float((sum-m)/m)#float((sum - int(money) * 10000)/(int(money) * 10000))
   r = round(r, ndigits=2)
   RobotReturn.objects.create(re=r)
   print('sum = '+ str(sum))
   print('r = '+ str(r))
   return HttpResponse()

# 2016第一季
'''
茂迪(2.6%) 中華電(21.4%) 遠傳(8.0%) 可成(5.8%) 全國電(12.1%) 國泰金(17.5%) 大聯大(6.1%) 康普(9.2%) 兆利(11.0%) 台產(6.3%)
0.05、0.05、0.08
s = ['6244', '2412', '4904', '2474', '6281', '2882', '3702', '4739', '3548', '2832']
n = [3, 13, 3, 5, 8, 10, 7, 7, 11, 11]
sum3=4905000
'''


def fund(request):
   name = ''
   loginstatus = False
   try:
        name = request.session['name']
        loginstatus = True
   except:
        return HttpResponseRedirect('/login/?back=資金管理')

   money = request.POST.get('invest', '500')
   type = RobotMember.objects.get(member_name=name).type #4
   stock = RobotStocks.objects.filter(type=type)
   sc = int(stock.count())
   id, mt, count,  mo= [], [], [], []
   for i in stock:
       id.append(i.stock_num)
       mt.append(i.type)
       count.append(sc)
       mo.append(money)
   #報酬率: 0.05、0.05、0.08
   #history, s, n, m= main(sc, id, type, count, money)
   #history = {'season':'2015Q2', 'invest':'台灣大(2.1%) 永昕(8.9%) 裕日車(26.2%) 致伸(3.9%) 震旦行(4.3%) 全國電(13.5%) 大聯大(9.5%) 強茂(0.9%) 兆利(7.6%) 鴻海(17.4%) 台產(5.8%) ', 'initial':'4802000.0'}
   #{'season':'2015Q3', 'invest':'台積電(4.8%) 鴻海(26.3%) 台塑(18.7%) 中華電(18.6%) 富邦(5.3%) 台灣大(3.6%) 遠傳(6.5%) 震旦行(3.5%) 台塑(11.4%) 強茂(2.2%) 兆利(5.8%) ', 'initial':'5562500'}
   s = ['6244', '2412', '4904', '2474', '6281', '2882', '3702', '4739', '3548', '2832']
   n = [3, 13, 3, 5, 8, 10, 7, 7, 11, 11]
   sum, sell_stock = 0.0, []  #賣價、 賣出的股票
   m = int(RobotTransactionInfo.objects.get(stock_id='6244', date='20160104').the_close)*3000 + int(RobotTransactionInfo.objects.get(stock_id='2412', date='20160104').the_close)*13000+ int(RobotTransactionInfo.objects.get(stock_id='4904', date='20160104').the_close)*3000 + int(RobotTransactionInfo.objects.get(stock_id='2474', date='20160104').the_close)*5000\
       + int(RobotTransactionInfo.objects.get(stock_id='6281', date='20160104').the_close)*8000 + int(RobotTransactionInfo.objects.get(stock_id='2882', date='20160104').the_close)*10000 + int(RobotTransactionInfo.objects.get(stock_id='3702', date='20160104').the_close)*7000 + int(RobotTransactionInfo.objects.get(stock_id='4739', date='20160104').the_close)*7000 \
       + int(RobotTransactionInfo.objects.get(stock_id='3548', date='20160104').the_close)*11000 + int(RobotTransactionInfo.objects.get(stock_id='2832', date='20160104').the_close)*11000

   #m = 5021200.0#5562500.0 #5756000
   print('money='+str(m))
   #for i in history:
        #Fund_set_history.objects.create(season=i['season'], invest=i['invest'], initial=i['initial'])
   for i, num in zip(s, n):
       name2 = RobotInformation.objects.get(stock_id=i).co_name
       pe_for_four_season = RobotPe.objects.get(date='2016Q1', stock_id=i).pe_for_four_season #2015Q1
       if pe_for_four_season == '--':
           pe_for_four_season = 0.0
       else:
           pe_for_four_season = float(pe_for_four_season) #201404
       #evl = float(Cash_Flows_Q.objects.get(date='201503', stock_id=i).free_cash_flows)*0.45 + pe_for_four_season*0.55
       '''if PE.objects.get(date='2015Q2', stock_id=i).coporate_estimated == '--' or Income_Statement_Q.objects.get(date='201502', stock_id=i).eps == '--':
           evl = (float(Transaction_info.objects.get(date='20150401', stock_id=i).the_close)+float(Transaction_info.objects.get(date='20150402', stock_id=i).the_close)+float(Transaction_info.objects.get(date='20150407', stock_id=i).the_close))/3.0
       else:
           evl = float(PE.objects.get(date='2015Q2', stock_id=i).coporate_estimated)*float(Income_Statement_Q.objects.get(date='201502', stock_id=i).eps) #本月(季)本益比*下月(季)每股盈餘
       '''
       dates = RobotTransactionInfo.objects.filter(date__startswith='201601', stock_id=i).order_by('date')
       count = dates.count()
       price_plus, price_minus = [], []
       for j in range(0, count):
          p = float(dates[j].the_close) #該股票在該月的股價
          price_plus.append(p)
          '''if p >= 0:
            price_plus.append(p)
          else:
            price_minus.append(p)'''
       #price_minus.reverse()
       price_plus.reverse()
       #for j in Transaction_info.objects.filter(date__startswith='201504', stock_id=i).order_by('date'): #201501
       for j in range(0, count): #201501
           evl = (float(dates[j].the_close) + float(dates[j+1].the_close) + float(dates[j+2].the_close)+ float(dates[j+3].the_close)+ float(dates[j+4].the_close))/5.0
           #evl2 = (float(dates[j+3].the_close) + float(dates[j+4].the_close) + float(dates[j+5].the_close))/3.0
           buy_price = float(RobotTransactionInfo.objects.filter(date__startswith='201601', stock_id=i).order_by('date')[0].the_close)
           if dates[j].the_close > evl:
               net = float(dates[j].the_close) -buy_price
               net = round(net, ndigits=2)
               net = net*1000*num
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               break
           elif dates[j].the_close == price_plus[0] or dates[j].the_close == price_plus[1] or dates[j].the_close == price_plus[2] or dates[j].the_close == price_plus[3]: #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               #print(evl)
               print('current=' + str(dates[j].the_close))
               print('buy=' + str(buy_price))
               break

           elif dates[j].the_close > buy_price*1.5 :#and dates[j].the_close > (evl2*1.5): #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               print('evl=' + str(evl))
               print('current=' + str(dates[j].the_close))
               print('buy=' + str(buy_price))
               break
           elif dates[j].the_close > buy_price*1.2 :#and dates[j].the_close > (evl2*1.2): #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               print(evl)
               print(dates[j].the_close)
               break
           '''elif dates[j].the_close > buy_price : #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               trade_2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               print(evl)
               print(dates[j].the_close)
               break'''

   for i in s:
       name2 = RobotInformation.objects.get(stock_id=i).co_name
       if i not in sell_stock:
           price = RobotTransactionInfo.objects.filter(date__startswith='201601', stock_id=i).order_by('date').last()
           date = price.date
           price = float(price.the_close)
           z = n[s.index(i)]
           net = price - float(RobotTransactionInfo.objects.filter(date__startswith='201601', stock_id=i).order_by('date').first().the_close)
           net = round(net, ndigits=2)
           net = int(net*1000*z)
           sell_stock.append(i)
           sum = sum + price*1000*z
           RobotTrade2015.objects.create(date=date, sell_stock=i+' '+name2, sell_price=price, stocks=z, net=net)
   #報酬率
   r = float((sum-m)/m)#float((sum - int(money) * 10000)/(int(money) * 10000))
   r = round(r, ndigits=2)
   RobotReturn.objects.create(re=r)
   print('sum = '+ str(sum))
   print('r = '+ str(r))

   sum, sell_stock = 0.0, []
   for i, num in zip(s, n):
       name2 = RobotInformation.objects.get(stock_id=i).co_name
       pe_for_four_season = RobotPe.objects.get(date='2016Q1', stock_id=i).pe_for_four_season
       if pe_for_four_season == '--':
           pe_for_four_season = 0.0
       else:
           pe_for_four_season = float(pe_for_four_season)
       #evl = float(Cash_Flows_Q.objects.get(date='201503', stock_id=i).free_cash_flows)*0.45 + pe_for_four_season*0.55
       '''if PE.objects.get(date='2015Q2', stock_id=i).coporate_estimated == '--' or Income_Statement_Q.objects.get(date='201502', stock_id=i).eps == '--':
           evl = (float(Transaction_info.objects.get(date='20150401', stock_id=i).the_close)+float(Transaction_info.objects.get(date='20150402', stock_id=i).the_close)+float(Transaction_info.objects.get(date='20150407', stock_id=i).the_close))/3.0
       else:
           evl = float(PE.objects.get(date='2015Q2', stock_id=i).coporate_estimated)*float(Income_Statement_Q.objects.get(date='201502', stock_id=i).eps) #本月(季)本益比*下月(季)每股盈餘
       '''
       dates = RobotTransactionInfo.objects.filter(date__startswith='201602', stock_id=i).order_by('date')
       count = dates.count()
       price_plus, price_minus = [], []
       for j in range(0, count):
          p = float(dates[j].the_close) #該股票在該月的股價
          price_plus.append(p)
          '''if p >= 0:
            price_plus.append(p)
          else:
            price_minus.append(p)'''
       #price_minus.reverse()
       price_plus.reverse()
       #for j in Transaction_info.objects.filter(date__startswith='201504', stock_id=i).order_by('date'): #201501
       for j in range(0, count): #201501
           evl = (float(dates[j].the_close) + float(dates[j+1].the_close) + float(dates[j+2].the_close)+ float(dates[j+3].the_close)+ float(dates[j+4].the_close))/5.0
           #evl2 = (float(dates[j+3].the_close) + float(dates[j+4].the_close) + float(dates[j+5].the_close))/3.0
           buy_price = float(RobotTransactionInfo.objects.filter(date__startswith='201602', stock_id=i).order_by('date')[0].the_close)
           if dates[j].the_close > evl:
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = net*1000*num
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               break
           elif dates[j].the_close == price_plus[0] :#or dates[j].the_close == price_plus[1] : #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)#-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               #print(evl)
               print('current=' + str(dates[j].the_close))
               print('buy=' + str(buy_price))
               break
           elif dates[j].the_close > buy_price*1.5 : #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               print('evl=' + str(evl))
               print('current=' + str(dates[j].the_close))
               print('buy=' + str(buy_price))
               break
           elif dates[j].the_close > buy_price*1.2 : #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               print(evl)
               print(dates[j].the_close)
               break
       '''for j in Transaction_info.objects.filter(date__startswith='201505', stock_id=i).order_by('date'):
           if j.the_close > (evl*2): #if j.the_close > (evl*1.5):
               net = float(j.the_close)-float(Transaction_info.objects.filter(date__startswith='201505', stock_id=i).order_by('date')[0].the_close)
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(j.the_close)*1000*num
               trade_2015.objects.create(date=j.date, sell_stock=i+' '+name2, sell_price=j.the_close, stocks=num, net=net)
               print(evl)
               print(j.the_close)
               break'''
   for i in s:
       name2 = RobotInformation.objects.get(stock_id=i).co_name
       if i not in sell_stock:
           price = RobotTransactionInfo.objects.filter(date__startswith='201602', stock_id=i).order_by('date').last()
           date = price.date
           price = float(price.the_close)
           z = n[s.index(i)]
           net = price - float(RobotTransactionInfo.objects.filter(date__startswith='201602', stock_id=i).order_by('date').first().the_close)
           net = round(net, ndigits=2)
           net = int(net*1000*z)
           sell_stock.append(i)
           sum = sum + price*1000*z
           RobotTrade2015.objects.create(date=date, sell_stock=i+' '+name2, sell_price=price, stocks=z, net=net)
   r = float((sum-m)/m)#float((sum - int(money) * 10000)/(int(money) * 10000))
   r = round(r, ndigits=2)
   RobotReturn.objects.create(re=r)
   print('sum = '+ str(sum))
   print('r = '+ str(r))

   '''if r > xx:
       money = xx
   mo = []
   for i in stock:
       mo.append(money)
   history, s, n = main(sc, id, type, count, money)'''
   sum, sell_stock = 0.0, []
   for i, num in zip(s, n):
       name2 = RobotInformation.objects.get(stock_id=i).co_name
       pe_for_four_season = RobotPe.objects.get(date='2016Q1', stock_id=i).pe_for_four_season
       if pe_for_four_season == '--':
           pe_for_four_season = 0.0
       else:
           pe_for_four_season = float(pe_for_four_season)
       #evl = float(Cash_Flows_Q.objects.get(date='201503', stock_id=i).free_cash_flows)*0.45 + pe_for_four_season*0.55
       '''if PE.objects.get(date='2015Q2', stock_id=i).coporate_estimated == '--' or Income_Statement_Q.objects.get(date='201502', stock_id=i).eps == '--':
           evl = (float(Transaction_info.objects.get(date='20150401', stock_id=i).the_close)+float(Transaction_info.objects.get(date='20150402', stock_id=i).the_close)+float(Transaction_info.objects.get(date='20150407', stock_id=i).the_close))/3.0
       else:
           evl = float(PE.objects.get(date='2015Q2', stock_id=i).coporate_estimated)*float(Income_Statement_Q.objects.get(date='201502', stock_id=i).eps) #本月(季)本益比*下月(季)每股盈餘
       '''
       dates = RobotTransactionInfo.objects.filter(date__startswith='201603', stock_id=i).order_by('date')
       count = dates.count()
       price_plus, price_minus = [], []
       for j in range(0, count):
          p = float(dates[j].the_close) #該股票在該月的股價
          price_plus.append(p)
          '''if p >= 0:
            price_plus.append(p)
          else:
            price_minus.append(p)'''
       #price_minus.reverse()
       price_plus.reverse()
       #for j in Transaction_info.objects.filter(date__startswith='201504', stock_id=i).order_by('date'): #201501
       for j in range(0, count): #201501
           evl = (float(dates[j].the_close) + float(dates[j+1].the_close) + float(dates[j+2].the_close)+ float(dates[j+3].the_close)+ float(dates[j+4].the_close))/5.0
           #evl2 = (float(dates[j+3].the_close) + float(dates[j+4].the_close) + float(dates[j+5].the_close))/3.0
           buy_price = float(RobotTransactionInfo.objects.filter(date__startswith='201603', stock_id=i).order_by('date')[0].the_close)
           if dates[j].the_close > evl:
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = net*1000*num
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               break
           elif dates[j].the_close == price_plus[0] : #or dates[j].the_close == price_plus[1]: #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               #print(evl)
               print('current=' + str(dates[j].the_close))
               print('buy=' + str(buy_price))
               break
           elif dates[j].the_close > buy_price*1.5 : #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               print('evl=' + str(evl))
               print('current=' + str(dates[j].the_close))
               print('buy=' + str(buy_price))
               break
           elif dates[j].the_close > buy_price*1.2 : #if j.the_close > (evl*1.5):  dates[j].the_close < (evl*1.5)
               net = float(dates[j].the_close)-buy_price
               net = round(net, ndigits=2)
               net = int(net*1000*num)
               sell_stock.append(i)
               sum = sum + float(dates[j].the_close)*1000*num
               RobotTrade2015.objects.create(date=dates[j].date, sell_stock=i+' '+name2, sell_price=dates[j].the_close, stocks=num, net=net)
               print(evl)
               print(dates[j].the_close)
               break
   for i in s:
       name2 = RobotInformation.objects.get(stock_id=i).co_name
       if i not in sell_stock:
           price = RobotTransactionInfo.objects.filter(date__startswith='201603', stock_id=i).order_by('date').last()
           date = price.date
           price = float(price.the_close)
           z = n[s.index(i)]
           net = price - float(RobotTransactionInfo.objects.filter(date__startswith='201603', stock_id=i).order_by('date').first().the_close)
           net = round(net, ndigits=2)
           net = int(net*1000*z)
           sell_stock.append(i)
           sum = sum + price*1000*z
           RobotTrade2015.objects.create(date=date, sell_stock=i+' '+name2, sell_price=price, stocks=z, net=net)
   r = float((sum-m)/m)#float((sum - int(money) * 10000)/(int(money) * 10000))
   r = round(r, ndigits=2)
   RobotReturn.objects.create(re=r)
   print('sum = '+ str(sum))
   print('r = '+ str(r))
   return HttpResponse()


def portfolio(request):
    name = ''
    loginstatus = False
    member = ''
    try:
         name = request.session['name']
         member = RobotMember.objects.get(member_name=name).member_id
         loginstatus = True
    except:
        return HttpResponseRedirect('/login/?back=My_News')
    return render_to_response('info3.html')


def fundamental_information(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    identity = request.GET.get('id', '2330')
    data = RobotInformation.objects.get(stock_id=identity)
    industry = RobotCategory.objects.get(category_id=data.category).category_name
    return render_to_response('info.html', {'industry': industry, 'stock': data, 'id': identity, 'name': name, 'loginstatus': loginstatus})


def fund_2(request):
   name = ''
   loginstatus = False
   try:
        name = request.session['name']
        loginstatus = True
   except:
        return HttpResponseRedirect('/login/?back=資金管理')
   type_id = RobotMember.objects.get(member_name=name).type
   type_name = RobotFqType.objects.get(type_id=type_id).type_name
   history, history2, trade, trade2, r = RobotFundSetHistory.objects.filter(season__startswith='2015'), RobotFundSetHistory.objects.filter(season__startswith='2016'), RobotTrade2015.objects.filter(date__startswith='2015'), RobotTrade2015.objects.filter(date__startswith='2016'), RobotReturn.objects.all()
   m, n, m2,gross_profit, gross_loss, month = [], [], [], [], [], []
   countp, countl, date_max, date_min, default, default2, default3 = 0, 0, '', '', '', '', '尚未設定'
   for i in RobotFundSet2016.objects.all():
       n.append(i)
   for i in range(0, 12):
       m.append(r[i].re)
   for i in range(12, 21):
       m2.append(r[i].re)
   for i in trade:
       if i.net > 0:
           gross_profit.append(i.net)
           countp = countp + 1
       elif i.net < 0:
           gross_loss.append(i.net)
           countl = countl + 1
       month.append(i.net)
   date_max, date_min = RobotTrade2015.objects.get(net=max(gross_profit)).date, RobotTrade2015.objects.get(net=min(gross_loss)).date
   mean, mean2, std, std2 = round(np.mean(m), ndigits=2), round(np.mean(m2), ndigits=2),round(np.std(m), ndigits=2),round(np.std(m2), ndigits=2)
   if type_id == '4':
       type_id = 7.5
   elif type_id == '1':
       type_id = 2
   elif type_id == '2':
       type_id = 4.5
   elif type_id == '3':
       type_id = 6
   else:
       type_id = 9.5
   p = 0
   if RobotSaveFund.objects.filter(name=name):
       default = RobotSaveFund.objects.last().invest
       default2 = RobotSaveFund.objects.last().strategy
   if request.method == 'POST':
       save = request.POST.get('b2', '0')
       invest = request.POST.get('invest', '500')
       category = request.POST.get('category', '')
       start = request.POST.get('b1', '0')
       if save == '0':
          save = '無'
          RobotSaveFund.objects.create(name=name, type=type_name, invest=invest, strategy=save)
       elif save == '1':
          save = '凱利公式'
          RobotSaveFund.objects.create(name=name, type=type_name, invest=invest, strategy=save)
       elif save == '2':
          save = '反秧策略'
          RobotSaveFund.objects.create(name=name, type=type_name, invest=invest, strategy=save)
       elif save == '3':
          save = 'Larry Williams'
          RobotSaveFund.objects.create(name=name, type=type_name, invest=invest, strategy=save)
       else:
          save = '固定比例法'
          RobotSaveFund.objects.create(name=name, type=type_name, invest=invest, strategy=save)

       if category == '0':
          category = '尚未設定'
          default3 = category
       elif category == '1':
          save = '凱利公式'
          default3 = category
       elif category == '2':
          category = '反秧策略'
          default3 = category
       elif category == '3':
          category = 'Larry Williams'
          default3 = category
       else:
          category = '固定比例法'
          default3 = category

       if start == '1':
           ranges = []
           for i in range(0, len(m)-3, 3):
               ranges.append(i)
           a = history.exclude(season='2015Q1')
           b = history.first()
           history = []
           history.append({'season':b.season, 'invest':b.invest, 'initial':int(b.initial)})
           for i, j in zip(ranges, a):
               sum1 = m[i] + m[i+1] + m[i+2]
               sum2 = m[i+3] + m[i+4] + m[i+5]
               if sum2 > sum1:
                   history.append({'season':j.season, 'invest':j.invest, 'initial':int(int(j.initial)*1.1)})
               elif sum2 < sum1:
                   history.append({'season':j.season, 'invest':j.invest, 'initial':int(int(j.initial)*0.9)})
               else:
                   history.append({'season':j.season, 'invest':j.invest, 'initial':int(j.initial)})
   return render_to_response('info3.html', {'loginstatus': loginstatus, 'name': name, 'history': history, 'history2': history2, 'return': r, 'mean': mean, 'mean2': mean2, 'std': std, 'std2': std2, 'type_name':type_name, 'type_id': type_id, 'now': n, 'trade2': trade2, 'sum': int(sum(m)),
                                            'gross_profit': sum(gross_profit), 'gross_loss': sum(gross_loss)*-1, 'month': int(np.mean(month)), 'max_profit': max(gross_profit), 'max_loss': min(gross_loss)*-1, 'count': countp+countl,
                                            'countp': countp, 'countl': countl, 'mean_profit': int(np.mean(gross_profit)), 'mean_loss': int(np.mean(gross_loss)*-1), 'average': abs(round(np.mean(gross_profit)/np.mean(gross_loss), ndigits=2)),
                                            'date_max':date_max, 'date_min':date_min, 'average2':round(sum(gross_profit)/(sum(gross_loss)*-1), ndigits=2), 'p':p, 'default':default, 'default2':default2, 'default3':default3})


def predict(request):
   name = ''
   loginstatus = False
   try:
        name = request.session['name']
        loginstatus = True
   except:
        return HttpResponseRedirect('/login/?back=未來型預測')
   category_id = RobotMember.objects.get(member_name=name).type
   cname = RobotFqType.objects.get(type_id=category_id).type_name
   if request.method == 'POST':
        stock = request.POST.get('stock', '')
        stock = stock[0:4]
        period = request.POST.get('myCheckBox', '')
        item1 = request.POST.get('myCheckBox2', '')
        paragraph1 = '本系統預測功能使用線性回歸模型來為使用者預測每股盈餘，使用者可參考此預測結果來決定要買進或賣出股票'
        if period == 'season' and item1 == 'profit':
            predict, search, past, industry_avg, std, category_name, score, next_season = predict_eps_season(stock)
            return render_to_response('predict2.html', {'paragraph1': paragraph1,'predict_type': '獲利能力', 'id': stock, 'predict': predict, 'search': search, 'past': past, 'industry_avg': industry_avg, 'std': std, 'category_name': category_name, 'score': score, 'next': next_season, 'season': '季','loginstatus': loginstatus, 'name': name})
        if period == 'year' and item1 == 'profit':
            predict, search, past, industry_avg, std, category_name, score, next_year = predict_eps_year(stock)
            return render_to_response('predict2.html', {'paragraph1': paragraph1,'predict_type': '獲利能力', 'id': stock, 'predict': predict, 'search': search, 'past': past, 'industry_avg': industry_avg, 'std': std, 'category_name': category_name, 'score': score, 'next': next_year, 'season': '年','loginstatus': loginstatus, 'name': name})

   return render_to_response('predict.html', {'cname': cname, 'loginstatus': loginstatus, 'name': name})


# 股票一產業分析: 表單
def analysis1(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass

    if loginstatus == True:
        type = RobotMember.objects.get(member_name=name).type
        your_type = RobotFqType.objects.get(type_id=type).type_name
        return render_to_response('analysis.html', {'type_name': your_type, 'name': name, 'loginstatus': loginstatus})
    else:
        return render_to_response('login.html')


# 股票一產業分析: 結果
def analysis2(request):
    ana = RobotAnalysis.objects.all()
    count = RobotAnalysis.objects.all().count()
    stock = [] #適合的股票類型
    stock1 = []
    #your_type = ''
    name = ''
    loginstatus = False
    category_name = 0
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass

    type = RobotMember.objects.get(member_name=name).type
    member = RobotMember.objects.get(member_name=name).member_id

    if request.method == 'POST':
        category = request.POST.get('category', '0')
        check1 = request.POST.get('check1', 0)
        stock_name = request.POST.get('stock_name', 0)
        #check2 = request.POST.get('check2', 0) #2
        pe = RobotPe.objects.all()
        if category != '0':
            category_name = RobotCategory.objects.get(category_id=category).category_name
        if category == '24' and check1 == '1':  #半導體業  #基本面診斷
            add1 = request.POST.get('2330', 0)
            add2 = request.POST.get('2344', 0)
            add3 = request.POST.get('2379', 0)
            add4 = request.POST.get('2454', 0)
            add5 = request.POST.get('2481', 0)

            for n in range(0, count):
                type_now = ana[n].type
                if type_now != type:
                    stock1.append(ana[n])
                else:
                    stock.append(ana[n]) #使用者適合的股票
            last = '強茂'#stock[-1]  抓最後一筆資料
            '''if type == '4':
                stock = ['台積電', '震旦行', '中華電信', '可成科技']'''

            your_type = RobotFqType.objects.get(type_id=type).type_name #顯示使用者為哪型
            return render_to_response('analysis2.html', {'last': last, 'category_name': category_name, 'ana': ana,'stock': stock, 'type': your_type, 'name': name, 'loginstatus': loginstatus})

        if category == '17' and check1 == '1':  #半導體業  #基本面診斷
            ana = RobotAnalysis2.objects.all()
            count = RobotAnalysis2.objects.all().count()
            for n in range(0, count):
                type_now = ana[n].type
                if type_now != type:
                    stock1.append(ana[n])
                else:
                    stock.append(ana[n]) #使用者適合的股票
            last = '國泰金'#stock[-1]  抓最後一筆資料
            your_type = RobotFqType.objects.get(type_id=type).type_name #顯示使用者為哪型
            return render_to_response('analysis2.html', {'last': last, 'category_name': category_name, 'ana': ana,'stock': stock, 'type': your_type, 'name': name, 'loginstatus': loginstatus})

        if stock_name != 0 and check1 == '1':  #輸入股號  #基本面診斷
            stock_name = stock_name[:4]
            category = RobotInformation.objects.get(stock_id=stock_name).category
            category_name = RobotCategory.objects.get(category_id=category).category_name
            st_type = RobotStocks.objects.get(stock_num=stock_name).type
            st_type2 = RobotFqType.objects.get(type_id=st_type).type_name
            if category == '24':
                RobotAna.objects.all().delete()
                ana0 = RobotAnalysis.objects.all()
                count = ana0.count()
                for i in range(0, count):
                    if ana0[i].stock_id == stock_name or ana0[i].stock_name == '同業平均':
                        RobotAna.objects.create(stock_id=ana0[i].stock_id, stock_name=ana0[i].stock_name, m0=ana0[i].m0, m1=ana0[i].m1, m2=ana0[i].m2, m3=ana0[i].m3, m4=ana0[i].m4, m5=ana0[i].m5,
                                           m6=ana0[i].m6, m7=ana0[i].m7, m8=ana0[i].m8, m9=ana0[i].m9, m10=ana0[i].m10, m11=ana0[i].m11, m12=ana0[i].m12, a1=ana0[i].a1, a2=ana0[i].a2, a3=ana0[i].a3, a4=ana0[i].a4, a5=ana0[i].a5)
                    #elif ana0[i].stock_id == 'mean':
                        #Ana.objects.create(ana0[i])
                count = RobotAna.objects.all().count()
                ana = RobotAna.objects.all()
            else:
                RobotAna.objects.all().delete()
                ana0 = RobotAnalysis2.objects.all()
                count = ana0.count()
                for i in range(0, count):
                    if ana0[i].stock_id == stock_name or ana0[i].stock_name == '同業平均':
                        RobotAna.objects.create(stock_id=ana0[i].stock_id, stock_name=ana0[i].stock_name, m0=ana0[i].m0, m1=ana0[i].m1, m2=ana0[i].m2, m3=ana0[i].m3, m4=ana0[i].m4, m5=ana0[i].m5,
                                           m6=ana0[i].m6, m7=ana0[i].m7, m8=ana0[i].m8, m9=ana0[i].m9, m10=ana0[i].m10, m11=ana0[i].m11, m12=ana0[i].m12, a1=ana0[i].a1, a2=ana0[i].a2, a3=ana0[i].a3, a4=ana0[i].a4, a5=ana0[i].a5)
                    #elif ana0[i].stock_id == 'mean':
                        #Ana.objects.create(ana0[i])
                count = RobotAna.objects.all().count()
                ana = RobotAna.objects.all()
            for n in range(0, count):
                type_now = ana[n].type
                if type_now != type:
                    stock1.append(ana[n])
                else:
                    stock.append(ana[n]) #使用者適合的股票
            last = '1'#stock[-1]  抓最後一筆資料
            ex = st_type2
            your_type = RobotFqType.objects.get(type_id=type).type_name #顯示使用者為哪型
            return render_to_response('analysis2.html', {'last': last, 'category_name': category_name, 'ana': ana,'stock': stock, 'type': your_type, 'name': name, 'loginstatus': loginstatus, 'ex': ex})

        if category == '24' and check1 == '2': #買賣時機分析
            list = ['2330', '2344', '2379', '2454', '2481']  #半導體的個股
            result = predict_eps_season2(list)  #預測是否會成長(1, 0)
            stock_name = []
            cheaps = []
            normals = []
            expensives = []
            prices = []
            signals = []
            a = []
            b = []
            f = []
            signal = '0'
            a_status = '0'
            b_status = '0'
            final = 0
            big = []
            ####### 計算合理價--本益比估價
            min0 = []
            max0 = []
            min1 = []
            max1 = []
            min2 = []
            max2 = []
            min3 = []
            max3 = []
            min4 = []
            max4 = []

            st_2330 = pe.filter(stock_id=list[0])
            for n in st_2330:
                min0.append(round(float(n.pe_low), ndigits=2))
                max0.append(round(float(n.pe_high), ndigits=2))

            st_2344 = pe.filter(stock_id=list[1])
            for n in st_2344:
                min1.append(round(float(n.pe_low), ndigits=2))
                max1.append(round(float(n.pe_high), ndigits=2))

            st_2379 = pe.filter(stock_id=list[2])
            for n in st_2379:
                min2.append(round(float(n.pe_low), ndigits=2))
                max2.append(round(float(n.pe_high), ndigits=2))

            st_2454 = pe.filter(stock_id=list[3])
            for n in st_2454:
                min3.append(round(float(n.pe_low), ndigits=2))
                max3.append(round(float(n.pe_high), ndigits=2))

            st_2481 = pe.filter(stock_id=list[4])
            for n in st_2481:
                min4.append(round(float(n.pe_low), ndigits=2))
                max4.append(round(float(n.pe_high), ndigits=2))

            # 2330
            min0 = np.mean(min0)  # 近5年最低本益比平均
            max0 = np.mean(max0)  # 近5年最高本益比平均
            mean0 = (min0 + max0)/2  # 平均本益比
            mean0_4Q = round(float(pe.get(stock_id=list[0], date='2016Q2').pe_for_four_season), ndigits=2) #前四季平均本益比

            #print(min0)
            #print(max0)
            #print(mean0)
            #print(mean0_4Q)
            cheap = mean0_4Q*min0
            expensive = mean0_4Q*max0
            normal = mean0_4Q*mean0
            #price = Transaction_info.objects.get(stock_id=list[0], date='20160826')
            share = Share(list[0]+'.TW')
            price = float(share.get_price()) # 即時股價
            if price > expensive: #被高估 : 賣(-)
                signal = '-'
            elif price < cheap: #被低估 : 買(+)
                signal = '+'
            else:
                signal = '0'
            #st0 = ['2330 台積電', cheap, normal, expensive, price, signal] #a_status, b_status, big, final

            #2330 技術面
            try:
                k_now = float(RobotTechnologyIndex2.objects.get(stock_id='2330', date='20160826').day_K)
                k_yes = float(RobotTechnologyIndex2.objects.get(stock_id='2330', date='20160825').day_K)
                d_now = float(RobotTechnologyIndex2.objects.get(stock_id='2330', date='20160826').day_D)
                d_yes = float(RobotTechnologyIndex2.objects.get(stock_id='2330', date='20160825').day_D)
            except:
                k_now = 0
                k_yes = 0
                d_now = 0
                d_yes = 0

            if k_now >= d_now and k_yes < d_yes : # 日KD黃金交叉
                a_status = '+'
            elif k_now < d_now and k_yes >= d_yes : # 日KD死亡交叉
                a_status = '-'
            else:
                a_status = '0'
            #st0.append(a_status)

            try:
                ma_now = float(RobotTechnologyIndex2.objects.get(stock_id='2330', date='20160826').day_MACD)
                ma_yes = float(RobotTechnologyIndex2.objects.get(stock_id='2330', date='20160825').day_MACD)
            except:
                ma_now = 0
                ma_yes = 0

            if ma_now > ma_yes : # 日MACD黃金交叉
                b_status = '+'
            elif ma_now < ma_yes : # 日MACD死亡交叉
                b_status = '-'
            else:
                b_status = '0'
            #st0.append(b_status)
            big.append('1') #是否為成長穩定企業
            #最終計算
            final = 0
            if result[0] == 1 and signal == '+':  # 未來是否繼續成長
                final = 2*(final + 1)  #2
            elif result[0] == 1 and signal == '0':
                final = final
            elif result[0] == 1 and signal == '-':
                final = final
            elif result[0] == 0 and signal == '+':
                final = final
            elif result[0] == 0 and signal == '0':
                final = final
            elif result[0] == 0 and signal == '-':
                final = 2*(final - 1)
            else:
                final = final
            if big[0] == '1':     #大型企業看估價signal
                if a_status == '+':
                    final = final + 1
                elif a_status == '-':
                    final = final - 1
                if b_status == '+':
                    final = final + 1
                elif b_status == '-':
                    final = final - 1
                if signal == '+':
                    final = final + 2
                elif a_status == '-':
                    final = final - 2
            else:
                if a_status == '+':
                    final = final + 2
                elif a_status == '-':
                    final = final - 2
                if b_status == '+':
                    final = final + 2
                elif b_status == '-':
                    final = final - 2
                if signal == '+':
                    final = final + 1
                elif a_status == '-':
                    final = final - 1

            # final >= 2代表有強烈買入訊號, big='1'較準確, result=1適合買進
            #st0.append(final)
            #st0 = ['2330 台積電', cheap, normal, expensive, price, signal] #a_status, b_status, big, final
            stock_name.append('台積電')
            cheaps.append(cheap)
            normals.append(normal)
            expensives.append(expensive)
            prices.append(price)
            signals.append(signal)
            a.append(a_status)
            b.append(b_status)
            f.append(final)
            print('f='+ str(f))

            '''print(cheap)
            print(normal)
            print(expensive)
            print(price)
            print(signal)
            print(a_status)
            print(b_status)
            print(final)
            print('#')
            print(cheaps)
            print(normals)
            print(expensives)'''

            # 2344
            print(min1)
            print(max1)
            min1 = np.mean(min1)  # 近5年最低本益比平均
            max1 = np.mean(max1)  # 近5年最高本益比平均
            mean1 = (min1 + max1)/2  # 平均本益比
            mean1_4Q = round(float(pe.get(stock_id=list[1], date='2016Q2').pe_for_four_season), ndigits=2) #前四季平均本益比

            cheap = round((mean1_4Q*min1)/10, ndigits=2)
            expensive = round((mean1_4Q*max1)/10, ndigits=2)
            normal = round((mean1_4Q*mean1)/10, ndigits=2)
            #price = float(Transaction_info.objects.get(stock_id=list[0], date='20160826').the_close)
            share = Share('2344'+'.TW')
            price = float(share.get_price())
            if price > expensive: #被高估 : 賣(-)
                signal = '-'
            elif price < cheap: #被低估 : 買(+)
                signal = '+'
            else:
                signal = '0'
            #st1 = ['2344 華邦電', cheap, normal, expensive, price, signal]

            #2344技術面
            try:
                k_now = float(RobotTechnologyIndex2.objects.get(stock_id='2344', date='20160826').day_K)
                k_yes = float(RobotTechnologyIndex2.objects.get(stock_id='2344', date='20160825').day_K)
                d_now = float(RobotTechnologyIndex2.objects.get(stock_id='2344', date='20160826').day_D)
                d_yes = float(RobotTechnologyIndex2.objects.get(stock_id='2344', date='20160825').day_D)
            except:
                k_now = 0
                k_yes = 0
                d_now = 0
                d_yes = 0

            if k_now >= d_now and k_yes < d_yes : # 日KD黃金交叉
                a_status = '+'
            elif k_now < d_now and k_yes >= d_yes : # 日KD死亡交叉
                a_status = '-'
            else:
                a_status = '0'
            #st1.append(a_status)

            try:
                ma_now = float(RobotTechnologyIndex2.objects.get(stock_id='2344', date='20160826').day_MACD)
                ma_yes = float(RobotTechnologyIndex2.objects.get(stock_id='2344', date='20160825').day_MACD)
            except:
                ma_now = 0
                ma_yes = 0

            if ma_now > ma_yes : # 日MACD黃金交叉
                b_status = '+'
            elif ma_now < ma_yes : # 日MACD死亡交叉
                b_status = '-'
            else:
                b_status = '0'
            #st1.append(b_status)
            big.append('0') #是否為成長穩定企業
            #最終計算
            final = 0
            if result[0] == 1 and signal == '+':  # 未來是否繼續成長
                final = 2*(final + 1)  #2
            elif result[0] == 1 and signal == '0':
                final = final
            elif result[0] == 1 and signal == '-':
                final = final
            elif result[0] == 0 and signal == '+':
                final = final
            elif result[0] == 0 and signal == '0':
                final = final
            elif result[0] == 0 and signal == '-':
                final = 2*(final - 1)
            else:
                final = final
            if big[0] == '1':     #大型企業看估價signal
                if a_status == '+':
                    final = final + 1
                elif a_status == '-':
                    final = final - 1
                if b_status == '+':
                    final = final + 1
                elif b_status == '-':
                    final = final - 1
                if signal == '+':
                    final = final + 2
                elif a_status == '-':
                    final = final - 2
            else:
                if a_status == '+':
                    final = final + 2
                elif a_status == '-':
                    final = final - 2
                if b_status == '+':
                    final = final + 2
                elif b_status == '-':
                    final = final - 2
                if signal == '+':
                    final = final + 1
                elif a_status == '-':
                    final = final - 1


            # final >= 2代表有強烈買入訊號, big='1'較準確, result=1適合買進
            #st1.append(final)
            stock_name.append('華邦電')
            cheaps.append(cheap)
            normals.append(normal)
            expensives.append(expensive)
            prices.append(price)
            signals.append(signal)
            a.append(a_status)
            b.append(b_status)
            f.append(final)

            print(cheap)
            print(normal)
            print(expensive)
            print(price)
            print(signal)
            print(a_status)
            print(b_status)
            print(final)
            print('#')
            print(cheaps)
            print(normals)
            print(expensives)
            print(min1)
            print(max1)
            print(mean1)
            print(mean1_4Q)


            # 2379
            min2 = np.mean(min2)  # 近5年最低本益比平均
            max2 = np.mean(max2)  # 近5年最高本益比平均
            mean2 = (min2 + max2)/2  # 平均本益比
            mean2_4Q = round(float(pe.get(stock_id=list[2], date='2016Q2').pe_for_four_season), ndigits=2) #前四季平均本益比

            #print(min0)
            #print(max0)
            #print(mean0)
            #print(mean0_4Q)
            cheap = round(mean2_4Q*min2*0.6, ndigits=2)
            expensive = round(mean2_4Q*max2*0.6, ndigits=2)
            normal = round(mean2_4Q*mean2*0.6, ndigits=2)
            #price = Transaction_info.objects.get(stock_id=list[0], date='20160826')
            share = Share(list[2]+'.TW')
            price = float(share.get_price()) # 即時股價
            if price > expensive: #被高估 : 賣(-)
                signal = '-'
            elif price < cheap: #被低估 : 買(+)
                signal = '+'
            else:
                signal = '0'
            #st0 = ['2330 台積電', cheap, normal, expensive, price, signal] #a_status, b_status, big, final

            #2379 技術面
            try:
                k_now = float(RobotTechnologyIndex2.objects.get(stock_id='2379', date='20160826').day_K)
                k_yes = float(RobotTechnologyIndex2.objects.get(stock_id='2379', date='20160825').day_K)
                d_now = float(RobotTechnologyIndex2.objects.get(stock_id='2379', date='20160826').day_D)
                d_yes = float(RobotTechnologyIndex2.objects.get(stock_id='2379', date='20160825').day_D)
            except:
                k_now = 0
                k_yes = 0
                d_now = 0
                d_yes = 0

            if k_now >= d_now and k_yes < d_yes : # 日KD黃金交叉
                a_status = '+'
            elif k_now < d_now and k_yes >= d_yes : # 日KD死亡交叉
                a_status = '-'
            else:
                a_status = '0'
            #st0.append(a_status)

            try:
                ma_now = float(RobotTechnologyIndex2.objects.get(stock_id='2379', date='20160826').day_MACD)
                ma_yes = float(RobotTechnologyIndex2.objects.get(stock_id='2379', date='20160825').day_MACD)
            except:
                ma_now = 0
                ma_yes = 0

            if ma_now > ma_yes : # 日MACD黃金交叉
                b_status = '+'
            elif ma_now < ma_yes : # 日MACD死亡交叉
                b_status = '-'
            else:
                b_status = '0'
            #st0.append(b_status)
            big.append('0') #是否為成長穩定企業
            #最終計算
            final = 0
            if result[0] == 1 and signal == '+':  # 未來是否繼續成長
                final = 2*(final + 1)  #2
            elif result[0] == 1 and signal == '0':
                final = final
            elif result[0] == 1 and signal == '-':
                final = final
            elif result[0] == 0 and signal == '+':
                final = final
            elif result[0] == 0 and signal == '0':
                final = final
            elif result[0] == 0 and signal == '-':
                final = 2*(final - 1)
            else:
                final = final
            if big[0] == '1':     #大型企業看估價signal
                if a_status == '+':
                    final = final + 1
                elif a_status == '-':
                    final = final - 1
                if b_status == '+':
                    final = final + 1
                elif b_status == '-':
                    final = final - 1
                if signal == '+':
                    final = final + 2
                elif a_status == '-':
                    final = final - 2
            else:
                if a_status == '+':
                    final = final + 2
                elif a_status == '-':
                    final = final - 2
                if b_status == '+':
                    final = final + 2
                elif b_status == '-':
                    final = final - 2
                if signal == '+':
                    final = final + 1
                elif a_status == '-':
                    final = final - 1


            # final >= 2代表有強烈買入訊號, big='1'較準確, result=1適合買進
            #st0.append(final)
            #st0 = ['2330 台積電', cheap, normal, expensive, price, signal] #a_status, b_status, big, final
            stock_name.append('瑞昱')
            cheaps.append(cheap)
            normals.append(normal)
            expensives.append(expensive)
            prices.append(price)
            signals.append(signal)
            a.append(a_status)
            b.append(b_status)
            f.append(final)


            # 2454
            min3 = np.mean(min3)  # 近5年最低本益比平均
            max3 = np.mean(max3)  # 近5年最高本益比平均
            mean3 = (min3 + max3)/2  # 平均本益比
            mean3_4Q = round(float(pe.get(stock_id=list[3], date='2016Q2').pe_for_four_season), ndigits=2) #前四季平均本益比

            #print(min0)
            #print(max0)
            #print(mean0)
            #print(mean0_4Q)
            cheap = round(mean3_4Q*min3*0.9, ndigits=2)
            expensive = round(mean3_4Q*max3*0.9, ndigits=2)
            normal = round(mean3_4Q*mean3*0.9, ndigits=2)
            #price = Transaction_info.objects.get(stock_id=list[0], date='20160826')
            share = Share(list[3]+'.TW')
            price = float(share.get_price()) # 即時股價
            if price > expensive: #被高估 : 賣(-)
                signal = '-'
            elif price < cheap: #被低估 : 買(+)
                signal = '+'
            else:
                signal = '0'
            #st0 = ['2330 台積電', cheap, normal, expensive, price, signal] #a_status, b_status, big, final

            #2379 技術面
            try:
                k_now = float(RobotTechnologyIndex2.objects.get(stock_id='2454', date='20160826').day_K)
                k_yes = float(RobotTechnologyIndex2.objects.get(stock_id='2454', date='20160825').day_K)
                d_now = float(RobotTechnologyIndex2.objects.get(stock_id='2454', date='20160826').day_D)
                d_yes = float(RobotTechnologyIndex2.objects.get(stock_id='2454', date='20160825').day_D)
            except:
                k_now = 0
                k_yes = 0
                d_now = 0
                d_yes = 0

            if k_now >= d_now and k_yes < d_yes : # 日KD黃金交叉
                a_status = '+'
            elif k_now < d_now and k_yes >= d_yes : # 日KD死亡交叉
                a_status = '-'
            else:
                a_status = '0'
            #st0.append(a_status)

            try:
                ma_now = float(RobotTechnologyIndex2.objects.get(stock_id='2454', date='20160826').day_MACD)
                ma_yes = float(RobotTechnologyIndex2.objects.get(stock_id='2454', date='20160825').day_MACD)
            except:
                ma_now = 0
                ma_yes = 0

            if ma_now > ma_yes : # 日MACD黃金交叉
                b_status = '+'
            elif ma_now < ma_yes : # 日MACD死亡交叉
                b_status = '-'
            else:
                b_status = '0'
            #st0.append(b_status)
            big.append('1') #是否為成長穩定企業
            #最終計算
            final = 0
            a_status = '+'
            if result[3] == 1 and signal == '+':  # 未來是否繼續成長
                final = 2*(final + 1)  #2
            elif result[3] == 1 and signal == '0':
                final = final
            elif result[3] == 1 and signal == '-':
                final = final
            elif result[3] == 0 and signal == '+':
                final = final
            elif result[3] == 0 and signal == '0':
                final = final
            elif result[3] == 0 and signal == '-':
                final = 2*(final - 1)
            else:
                final = final
            if big[3] == '1':     #大型企業看估價signal
                if a_status == '+':
                    final = final + 1
                elif a_status == '-':
                    final = final - 1
                if b_status == '+':
                    final = final + 1
                elif b_status == '-':
                    final = final - 1
                if signal == '+':
                    final = final + 2
                elif a_status == '-':
                    final = final - 2
            else:
                if a_status == '+':
                    final = final + 2
                elif a_status == '-':
                    final = final - 2
                if b_status == '+':
                    final = final + 2
                elif b_status == '-':
                    final = final - 2
                if signal == '+':
                    final = final + 1
                elif a_status == '-':
                    final = final - 1


            # final >= 2代表有強烈買入訊號, big='1'較準確, result=1適合買進
            #st0.append(final)
            #st0 = ['2330 台積電', cheap, normal, expensive, price, signal] #a_status, b_status, big, final
            stock_name.append('聯發科')
            cheaps.append(cheap)
            normals.append(normal)
            expensives.append(expensive)
            prices.append(price)
            signals.append(signal)
            a.append(a_status)
            b.append(b_status)
            f.append(final)


            # 2481
            min4 = np.mean(min4)  # 近5年最低本益比平均
            max4 = np.mean(max4)  # 近5年最高本益比平均
            mean4 = (min4 + max4)/2  # 平均本益比
            mean4_4Q = round(float(pe.get(stock_id=list[4], date='2016Q2').pe_for_four_season), ndigits=2) #前四季平均本益比

            #print(min0)
            #print(max0)
            #print(mean0)
            #print(mean0_4Q)
            cheap = round(mean4_4Q*min4, ndigits=2)
            expensive = round(mean4_4Q*max4, ndigits=2)
            normal = round(mean4_4Q*mean4, ndigits=2)
            #price = Transaction_info.objects.get(stock_id=list[0], date='20160826')
            share = Share(list[4]+'.TW')
            price = float(share.get_price()) # 即時股價
            if price > expensive: #被高估 : 賣(-)
                signal = '-'
            elif price < cheap: #被低估 : 買(+)
                signal = '+'
            else:
                signal = '0'
            #st0 = ['2330 台積電', cheap, normal, expensive, price, signal] #a_status, b_status, big, final

            #2379 技術面
            try:
                k_now = float(RobotTechnologyIndex2.objects.get(stock_id='2481', date='20160826').day_K)
                k_yes = float(RobotTechnologyIndex2.objects.get(stock_id='2481', date='20160825').day_K)
                d_now = float(RobotTechnologyIndex2.objects.get(stock_id='2481', date='20160826').day_D)
                d_yes = float(RobotTechnologyIndex2.objects.get(stock_id='2481', date='20160825').day_D)
            except:
                k_now = 0
                k_yes = 0
                d_now = 0
                d_yes = 0

            if k_now >= d_now and k_yes < d_yes : # 日KD黃金交叉
                a_status = '+'
            elif k_now < d_now and k_yes >= d_yes : # 日KD死亡交叉
                a_status = '-'
            else:
                a_status = '0'
            #st0.append(a_status)

            try:
                ma_now = float(RobotTechnologyIndex2.objects.get(stock_id='2481', date='20160826').day_MACD)
                ma_yes = float(RobotTechnologyIndex2.objects.get(stock_id='2481', date='20160825').day_MACD)
            except:
                ma_now = 0
                ma_yes = 0

            if ma_now > ma_yes : # 日MACD黃金交叉
                b_status = '+'
            elif ma_now < ma_yes : # 日MACD死亡交叉
                b_status = '-'
            else:
                b_status = '0'
            #st0.append(b_status)
            big.append('0') #是否為成長穩定企業
            #最終計算
            final = 0
            if result[4] == 1 and signal == '+':  # 未來是否繼續成長
                final = 2*(final + 1)  #2
            elif result[4] == 1 and signal == '0':
                final = final
            elif result[4] == 1 and signal == '-':
                final = final
            elif result[4] == 0 and signal == '+':
                final = final
            elif result[4] == 0 and signal == '0':
                final = final
            elif result[4] == 0 and signal == '-':
                final = 2*(final - 1)
            else:
                final = final
            if big[4] == '1':     #大型企業看估價signal
                if a_status == '+':
                    final = final + 1
                elif a_status == '-':
                    final = final - 1
                if b_status == '+':
                    final = final + 1
                elif b_status == '-':
                    final = final - 1
                if signal == '+':
                    final = final + 2
                elif a_status == '-':
                    final = final - 2
            else:
                if a_status == '+':
                    final = final + 2
                elif a_status == '-':
                    final = final - 2
                if b_status == '+':
                    final = final + 2
                elif b_status == '-':
                    final = final - 2
                if signal == '+':
                    final = final + 1
                elif a_status == '-':
                    final = final - 1

            # final >= 2代表有強烈買入訊號, big='1'較準確, result=1適合買進
            #st0.append(final)
            #st0 = ['2330 台積電', cheap, normal, expensive, price, signal] #a_status, b_status, big, final
            stock_name.append('強茂')
            cheaps.append(cheap)
            normals.append(normal)
            expensives.append(expensive)
            prices.append(price)
            signals.append(signal)
            a.append(a_status)
            b.append(b_status)
            f.append(final)
            print(big)


            for n in range(0, count):
                type_now = ana[n].type
                if type_now != type:
                    stock1.append(ana[n])
                else:
                    stock.append(ana[n]) #使用者適合的股票
            last = '強茂'#stock[-1]  抓最後一筆資料
            print(f)
            c1 = len(list)
            your_type = RobotFqType.objects.get(type_id=type).type_name #顯示使用者為哪型
            return render_to_response('analysis2_buy.html', {'c1': range(0,c1), 'last': '強茂', 'category_name': category_name, 'ana': ana,'stock': stock, 'type': your_type, 'stock_name': stock_name, 'cheaps': cheaps, 'normals': normals, 'expensives': expensives, 'prices': prices, 'signals': signals, 'a': a, 'b': b, 'f': f, 'big': big, 'result': result, 'name': name, 'loginstatus': loginstatus})


def add(request): #健診機器人--加入追蹤

            name = request.session['name']
            member = RobotMember.objects.get(member_name=name).member_id

            stock_status = 0
            content = RobotTrackStock.objects.filter(member_id=member)

            add1 = request.POST.get('2330', 0)
            add2 = request.POST.get('2344', 0)
            add3 = request.POST.get('2379', 0)
            add4 = request.POST.get('2454', 0)
            add5 = request.POST.get('2481', 0)
            if add1 != 0:
                if len(content) == 0:  # 沒有加過 任何股票(資料庫沒有資料)
                    RobotTrackStock.objects.create(member_id=member, stock_id='2330')
                else:
                    for n in range(0, len(content)):
                        if '2330' != content[n].stock_id:
                            stock_status = stock_status + 1
                        if stock_status == len(content):
                            RobotTrackStock.objects.create(member_id=member, stock_id='2330')

            if add2 != 0:
                if len(content) == 0:  # 沒有加過 任何股票(資料庫沒有資料)
                    RobotTrackStock.objects.create(member_id=member, stock_id='2344')
                else:
                    for n in range(0, len(content)):
                        if '2330' != content[n].stock_id:
                            stock_status = stock_status + 1
                        if stock_status == len(content):
                            RobotTrackStock.objects.create(member_id=member, stock_id='2344')
            if add3 != 0:
                if len(content) == 0:  # 沒有加過 任何股票(資料庫沒有資料)
                    RobotTrackStock.objects.create(member_id=member, stock_id='2379')
                else:
                    for n in range(0, len(content)):
                        if '2379' != content[n].stock_id:
                            stock_status = stock_status + 1
                        if stock_status == len(content):
                            RobotTrackStock.objects.create(member_id=member, stock_id='2379')
            if add4 != 0:
                if len(content) == 0:  # 沒有加過 任何股票(資料庫沒有資料)
                    RobotTrackStock.objects.create(member_id=member, stock_id='2454')
                else:
                    for n in range(0, len(content)):
                        if '2454' != content[n].stock_id:
                            stock_status = stock_status + 1
                        if stock_status == len(content):
                            RobotTrackStock.objects.create(member_id=member, stock_id='2454')
            if add5 != 0:
                if len(content) == 0:  # 沒有加過 任何股票(資料庫沒有資料)
                    RobotTrackStock.objects.create(member_id=member, stock_id='2481')
                else:
                    for n in range(0, len(content)):
                        if '2481' != content[n].stock_id:
                            stock_status = stock_status + 1
                        if stock_status == len(content):
                            RobotTrackStock.objects.create(member_id=member, stock_id='2481')
            name = ''
            loginstatus = False
            try:
                 name = request.session['name']
                 loginstatus = True
            except:
                  pass

            if loginstatus == True:
                type = RobotMember.objects.get(member_name=name).type
                your_type = RobotFqType.objects.get(type_id=type).type_name
                return render_to_response('analysis.html', {'type_name': your_type, 'name': name, 'loginstatus': loginstatus})
            else:
                return render_to_response('login.html')


def gep(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass

    if loginstatus == True:
        type = RobotMember.objects.get(member_name=name).type
        your_type = RobotFqType.objects.get(type_id=type).type_name
        elec = request.GET.get('elec', '0')
        no_elec = request.GET.get('no_elec', '0')
        if request.method == 'GET' and request.GET.get('btn', 0)== '1': #年
            if elec == no_elec:
                stock_type = RobotStocks.objects.filter(type=type) #符合投資人屬性的股票
                elec = '電子&非電子類股'
            elif elec == '1':
                stock_type = RobotStocks.objects.filter(type=type, elec='1') #符合投資人屬性&電子類股的股票
                elec = '電子類股'
            elif no_elec == '1':
                stock_type = RobotStocks.objects.filter(type=type, elec='0') #符合投資人屬性&非電子類股的股票
                elec = '非電子類股'
            stock_credit = [] #第二層篩選
            stock_good = [] #$回傳好股票
            stock_soso = [] #$回傳次等股票
            s1 = []  #$好股票總評
            s2 = []  #$次等股票總評
            cat1 = []  #$好股票產業
            cat2 = []  #$次等股票產業
            d = []

            #選擇排名前50上市櫃公司
            for n in stock_type:
                if n.credit_type != '0':
                    stock_credit.append(n.stock_num)
            for i in stock_credit: #i是股號
                co_name = RobotInformation.objects.get(stock_id= i).co_name #股名
                category1 = RobotInformation.objects.get(stock_id= i).co_market #上市櫃
                category = RobotInformation.objects.get(stock_id= i).category #抓產業(不加)
                category2 = RobotCategory.objects.get(category_id=category).category_name #產業
                c0 = float(RobotRatio1.objects.get(stock_id= i, date='2015').ROE) #roe
                c1 = float(RobotIncomeStatement.objects.get(stock_id= i, date='2015').eps)
                c2 = float(RobotRatio1.objects.get(stock_id= i, date='2015').operating_profit_ratio) #營業利益率
                c3 = float(RobotRatio1.objects.get(stock_id= i, date='2015').gross_margin)
                c4 = float(RobotRatio1.objects.get(stock_id= i, date='2015').pretax_net_profit_margin)
                c5 = float(RobotRatio4.objects.get(stock_id= i, date='2015').debt_ratio)
                c6 = float(RobotRatio4.objects.get(stock_id= i, date='2015').current_ratio)
                c7 = float(RobotRatio2.objects.get(stock_id= i, date='2015').revenue_growth_ratio)
                c8 = 0
                c9 = 0
                if RobotRatio3.objects.get(stock_id= i, date='2015').accounts_receivable_turnover_ratio != '--':
                    c8 = float(RobotRatio3.objects.get(stock_id= i, date='2015').accounts_receivable_turnover_ratio)
                if RobotRatio3.objects.get(stock_id= i, date='2015').inventory_turnover_ratio != '--':
                    c9 = float(RobotRatio3.objects.get(stock_id= i, date='2015').inventory_turnover_ratio)

                c10 = float(RobotRatio3.objects.get(stock_id= i, date='2015').fixed_asset_turnover_ratio)
                c11 = float(RobotPe.objects.get(stock_id= i, date='2016Q1').pe_for_four_season)
                c12 = 0
                d = [c0, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12]
                stock_class = gepModel(d) #一個股票一個結果:0, 1

                score = 0

                if c0 >= RobotMean.objects.get(id='1').m0:
                    score = score+1
                if c1 >= RobotMean.objects.get(id='1').m1:
                    score = score+1
                if c2 >= RobotMean.objects.get(id='1').m2:
                    score = score+1
                if c3 >= RobotMean.objects.get(id='1').m3:
                    score = score+1
                if c4 >= RobotMean.objects.get(id='1').m4:
                    score = score+1
                if c5 <= RobotMean.objects.get(id='1').m5:
                    score = score+1
                if c6 <= RobotMean.objects.get(id='1').m6:
                    score = score+1
                if c7 <= RobotMean.objects.get(id='1').m7:
                    score = score+1
                if c8 <= RobotMean.objects.get(id='1').m8:
                    score = score+1
                if c9 <= RobotMean.objects.get(id='1').m9:
                    score = score+1
                if c10 <= RobotMean.objects.get(id='1').m10:
                    score = score+1
                if c11 <= RobotMean.objects.get(id='1').m11:
                    score = score+1

                if stock_class == 1:
                    if score >= 4:
                        a = RobotInformation.objects.get(stock_id=i).category
                        cat1.append(RobotCategory.objects.get(category_id=a).category_name)
                        stock_good.append(RobotInformation.objects.get(stock_id=i)) #好股票的股號
                        if score >= 5:
                           s1.append('5')
                        else:
                           s1.append('4.5')

                    elif score < 4 and score >=2:
                        a = RobotInformation.objects.get(stock_id=i).category
                        cat2.append(RobotCategory.objects.get(category_id=a).category_name)
                        stock_soso.append(RobotInformation.objects.get(stock_id=i))  #較差的股號 stock_good.co_name/ category
                        if score >= 4:
                            s2.append('4')
                        else:
                            s2.append('3')

            count1 = len(stock_good)  #$好股票個數
            count2 = len(stock_soso)  #$次等股票個數
            #count = count1 + count2
            print(count1)
            print(count2)
            print(stock_good)
            print(stock_soso)
            print(cat1)
            print(cat2)
            print(s1)
            print(s2)
            return render_to_response('gep_elec.html', {'count1': count1,'count2': count2,'c1': range(0,count1),'c2': range(0,count2),'cat1': cat1,'cat2': cat2,'s1': s1,'s2': s2,'type': your_type,'stock_good': stock_good,'stock_soso': stock_soso, 'name': name, 'loginstatus': loginstatus, 'elec': elec})
        else:
            return render_to_response('gep_elec.html', {'type': your_type, 'name': name, 'loginstatus': loginstatus})

    else :
        return render_to_response('login.html')


def add3(request): #gep 加入追蹤
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    if loginstatus == True:
        type = RobotMember.objects.get(member_name=name).type
        member_id = RobotMember.objects.get(member_name=name).member_id
        your_type = RobotFqType.objects.get(type_id=type).type_name
        stock_status = 0
        content = RobotTrackStock.objects.filter(member_id=member_id)
        if request.method == 'POST' and request.POST.get('btn2', 0)== '1':
            count1 = int(request.POST.get('count1'))
            count2 = int(request.POST.get('count2'))
            for i in range(0,count1):  #優良
                add = request.POST.get(str(i))
                if add != None:
                    if len(content) == 0:  # 沒有加過 任何股票(資料庫沒有資料)
                        RobotTrackStock.objects.create(member_id=member_id, stock_id=add)
                    else:
                        for n in range(0, len(content)):
                            if add != content[n].stock_id:
                                stock_status = stock_status + 1
                            if stock_status == len(content):
                                RobotTrackStock.objects.create(member_id=member_id, stock_id=add)

            for i in range(0,count2):  #次等
                add = request.POST.get('5'+str(i))
                if add != None:
                    if len(content) == 0:  # 沒有加過 任何股票(資料庫沒有資料)
                        RobotTrackStock.objects.create(member_id=member_id, stock_id=add)
                    else:
                        for n in range(0, len(content)):
                            if add != content[n].stock_id:
                                stock_status = stock_status + 1
                            if stock_status == len(content):
                                RobotTrackStock.objects.create(member_id=member_id, stock_id=add)

        return render_to_response('gep1.html', {'type': your_type, 'name': name, 'loginstatus': loginstatus})
    return render_to_response('login.html')


def fq(request):
   name = ''
   loginstatus = False
   try:
        name = request.session['name']
        loginstatus = True
   except:
        pass
   sum = 0
   if request.method == 'POST':
       q1 = request.POST.get('q1', '')
       q2 = request.POST.get('q2', '')
       q3 = request.POST.get('q3', '')
       q4 = request.POST.get('q4', '')
       q5 = request.POST.get('q5', '')
       q6 = request.POST.get('q6', '')
       q7 = request.POST.get('q7', '')

       if q1 is '' or q2 is '' or q3 is '' or q4 is '' or q5 is '' or q6 is '' or q7 is '':
           status = False
           message = '您尚有題目未作答，請重新確認'
           return render_to_response('test.html', {'loginstatus': loginstatus, 'name': name, 'message': message, 'status': status})
       else:
           q1 = int(q1)
           q2 = int(q2)
           q3 = int(q3)
           q4 = int(q4)
           q5 = int(q5)
           q6 = int(q6)
           q7 = int(q7)
           sum = q1 + q2 + q3 + q4 + q5 + q6 + q7
           if sum in range(0, 11):
               try:
                   RobotMember.objects.filter(member_name=name).update(type = '1')
               except:
                   pass
               return render_to_response('test_result.html', {'loginstatus': loginstatus, 'name': name, 'sum': sum})
           elif sum in range(11, 16):
               try:
                   RobotMember.objects.filter(member_name=name).update(type = '2')
               except:
                   pass
               return render_to_response('test_result2.html', {'loginstatus': loginstatus, 'name': name, 'sum': sum})
           elif sum in range(16, 23):
               try:
                   RobotMember.objects.filter(member_name=name).update(type = '3')
               except:
                   pass
               return render_to_response('test_result3.html', {'loginstatus': loginstatus, 'name': name, 'sum': sum})
           elif sum in range(23, 31):
               try:
                   RobotMember.objects.filter(member_name=name).update(type = '4')
               except:
                   pass
               return render_to_response('test_result4.html', {'loginstatus': loginstatus, 'name': name, 'sum': sum})
           else:
               try:
                   RobotMember.objects.filter(member_name=name).update(type = '5')
               except:
                   pass
               return render_to_response('test_result5.html', {'loginstatus': loginstatus, 'name': name, 'sum': sum})

   return render_to_response('test.html', {'loginstatus': loginstatus, 'name': name})


def five_stock(request):
    name = ''
    loginstatus = False
    try:
         name = request.session['name']
         loginstatus = True
    except:
        pass
    price, TL, TL_SD, TL_2SD, TL_plus_SD, TL_plus_2SD, stock_name, click, today, date, stock_id, position, slope, tw, p = [], [], [], [], [], [], 0, 0, 0, 0, '', '', '', '', 0
    conclusion = ''
    today = datetime.now().strftime('%Y-%m-%d')
    print('today= '+today)
    if request.method == 'POST':
        stock_id = request.POST.get('stock_id', '')[0:4]
        stock_name = request.POST.get('stock_id', '')[5:]
        click = request.POST.get('draw')
        date = request.POST.get('date')[0:4]+'/'+request.POST.get('date')[5:7]+'/'+request.POST.get('date')[8:]
        print('date= '+date)
        if stock_id != '':
            try:
                tran = RobotFive.objects.filter(stock_id = stock_id)
                for i in tran:
                    price.append(round(i.the_close, ndigits=2))
                    TL.append(round(i.Price_TL, ndigits=2))
                    TL_SD.append(round(i.TL_SD, ndigits=2))
                    TL_2SD.append(round(i.TL_2SD, ndigits=2))
                    TL_plus_SD.append(round(i.TL_plus_SD, ndigits=2))
                    TL_plus_2SD.append(round(i.TL_plus_2SD, ndigits=2))
            except:
                tran = RobotFive.objects.filter(stock_id = '2330')
                for i in tran:
                    price.append(round(i.the_close, ndigits=2))
                    TL.append(round(i.Price_TL, ndigits=2))
                    TL_SD.append(round(i.TL_SD, ndigits=2))
                    TL_2SD.append(round(i.TL_2SD, ndigits=2))
                    TL_plus_SD.append(round(i.TL_plus_SD, ndigits=2))
                    TL_plus_2SD.append(round(i.TL_plus_2SD, ndigits=2))

            if date == '2016/08/26':
                p = price[len(price)-1] #股價
                #股價位置
                if p > TL_plus_2SD[len(TL)-1]:
                    position = '趨勢線兩個標準差以上'#股價位於<font color="red">趨勢線2個標準差
                elif p >= TL_plus_SD[len(TL)-1] and p < TL_plus_2SD[len(TL)-1]:
                    position = '趨勢線以上一到兩個標準差之間'
                elif p >= TL[len(TL)-1] and p < TL_plus_SD[len(TL)-1]:
                    position = '趨勢線以上到一個標準差之間'
                elif p >= TL_SD[len(TL)-1] and p < TL[len(TL)-1]:
                    position = '趨勢線以下一個標準差之間'
                elif p >= TL_2SD[len(TL)-1] and p < TL[len(TL)-1]:
                    position = '趨勢線以下一到兩個標準差之間'

                #趨勢線斜率
                if TL[len(TL)-1] >= TL[len(TL)-2]:
                    slope = '正斜率'
                else:
                    slope = '負斜率'

                #台股基本面
                tw = 'PBR、DY皆低於平均值'
                if position == '趨勢線以上到一個標準差之間' or position == '趨勢線以上一到兩個標準差之間':
                    conclusion = '未來股價上漲機率高，是不錯的買點'
                elif position == '趨勢線兩個標準差以上':
                    conclusion = '未來股價可能下跌，此時非買點而是賣點'
                elif position == '趨勢線以下一個標準差之間' or position == '趨勢線以下一到兩個標準差之間':
                    conclusion = '未來股價還有很大的上漲空間，可以考慮買進'
                elif position == '趨勢線以下兩個標準差之間':
                    conclusion = '未來股價可能上漲，此時非賣點而是買點'
            elif stock_id == '3008':

                date2 = request.POST.get('date')[0:4]+request.POST.get('date')[5:7]+request.POST.get('date')[8:]
                p = RobotFive.objects.get(stock_id = stock_id, date = date2).the_close #股價
                #股價位置
                if p > RobotFive.objects.get(stock_id = stock_id, date = date2).TL_plus_2SD:
                    position = '趨勢線兩個標準差以上'#股價位於<font color="red">趨勢線2個標準差
                elif p >= RobotFive.objects.get(stock_id = stock_id, date = date2).TL_plus_SD and p < RobotFive.objects.get(stock_id = stock_id, date = date2).TL_plus_2SD:
                    position = '趨勢線以上一到兩個標準差之間'
                elif p >= RobotFive.objects.get(stock_id = stock_id, date = date2).Price_TL and p < RobotFive.objects.get(stock_id = stock_id, date = date2).TL_plus_SD:
                    position = '趨勢線以上到一個標準差之間'
                elif p >= RobotFive.objects.get(stock_id = stock_id, date = date2).TL_SD and p < RobotFive.objects.get(stock_id = stock_id, date = date2).Price_TL:
                    position = '趨勢線以下一個標準差之間'
                elif p >= RobotFive.objects.get(stock_id = stock_id, date = date2).TL_2SD and p < RobotFive.objects.get(stock_id = stock_id, date = date2).Price_TL:
                    position = '趨勢線以下一到兩個標準差之間'

                #趨勢線斜率
                if RobotFive.objects.get(stock_id = stock_id, date = date2).a >= 0:
                    slope = '正斜率'
                else:
                    slope = '負斜率'

                #台股基本面
                tw = 'PBR、DY皆低於平均值'
                if position == '趨勢線以上到一個標準差之間' or position == '趨勢線以上一到兩個標準差之間':
                    conclusion = '未來股價上漲機率高，是不錯的買點'
                elif position == '趨勢線兩個標準差以上':
                    conclusion = '未來股價可能下跌，此時非買點而是賣點'
                elif position == '趨勢線以下一個標準差之間' or position == '趨勢線以下一到兩個標準差之間':
                    conclusion = '未來股價還有很大的上漲空間，可以考慮買進'
                elif position == '趨勢線以下兩個標準差之間':
                    conclusion = '未來股價可能上漲，此時非賣點而是買點'

            elif stock_id == '2330':

                date2 = request.POST.get('date')[0:4]+request.POST.get('date')[5:7]+request.POST.get('date')[8:]
                p = RobotFive.objects.get(stock_id = stock_id, date = date2).the_close #股價
                #股價位置
                if p > RobotFive.objects.get(stock_id = stock_id, date = date2).TL_plus_2SD:
                    position = '趨勢線兩個標準差以上'#股價位於<font color="red">趨勢線2個標準差
                elif p >= RobotFive.objects.get(stock_id = stock_id, date = date2).TL_plus_SD and p < RobotFive.objects.get(stock_id = stock_id, date = date2).TL_plus_2SD:
                    position = '趨勢線以上一到兩個標準差之間'
                elif p >= RobotFive.objects.get(stock_id = stock_id, date = date2).Price_TL and p < RobotFive.objects.get(stock_id = stock_id, date = date2).TL_plus_SD:
                    position = '趨勢線以上到一個標準差之間'
                elif p >= RobotFive.objects.get(stock_id = stock_id, date = date2).TL_SD and p < RobotFive.objects.get(stock_id = stock_id, date = date2).Price_TL:
                    position = '趨勢線以下一個標準差之間'
                elif p >= RobotFive.objects.get(stock_id = stock_id, date = date2).TL_2SD and p < RobotFive.objects.get(stock_id = stock_id, date = date2).Price_TL:
                    position = '趨勢線以下一到兩個標準差之間'
                else:
                    position = '趨勢線以下兩個標準差之間'

                #趨勢線斜率
                if RobotFive.objects.get(stock_id = stock_id, date = date2).a >= 0:
                    slope = '正斜率'
                else:
                    slope = '負斜率'

                #台股基本面
                tw = 'PBR、DY皆低於平均值'

                #結論

                if position == '趨勢線以上到一個標準差之間' or position == '趨勢線以上一到兩個標準差之間':
                    conclusion = '未來股價上漲機率高，是不錯的買點'
                elif position == '趨勢線兩個標準差以上':
                    conclusion = '未來股價可能下跌，此時非買點而是賣點'
                elif position == '趨勢線以下一個標準差之間' or position == '趨勢線以下一到兩個標準差之間':
                    conclusion = '未來股價還有很大的上漲空間，可以考慮買進'
                elif position == '趨勢線以下兩個標準差之間':
                    conclusion = '未來股價可能上漲，此時非賣點而是買點'



            return render_to_response('f.html', {'name': name, 'loginstatus': loginstatus, 'price': price, 'TL_plus_2SD': TL_plus_2SD, 'TL_plus_SD': TL_plus_SD, 'TL_2SD': TL_2SD, 'TL_SD': TL_SD
        , 'TL': TL, 'stock_name': stock_name, 'click': click, 'today': today, 'date': date, 'stock_id': stock_id, 'tw': tw, 'slope': slope, 'p': p, 'position': position, 'conclusion': conclusion})



