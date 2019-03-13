from django.shortcuts import render,render_to_response,HttpResponseRedirect,redirect

from .models import RobotMember,RobotYahooNew,RobotCna,RobotYahooHot,RobotYahooStock,RobotYahooTec,RobotYahooTra,RobotYahoo,RobotYahooTendency,RobotDiscuss,RobotInformation,RobotTransactionInfo,RobotCorporate,RobotTrackStock,RobotCategory
from django.contrib.auth import authenticate, login
from . import views
from django.views.generic import View
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.mail import send_mail
import random


def news_con(request):

    return render(request, 'news_con.html')

def home(request):

    return render(request, 'home.html')


# def home(request):  #理財小學堂
#    name = ''
#    loginstatus = False
#    try:
#         name = request.session['name']
#         loginstatus = True
#    except:
#         pass
#    return render_to_response('smallschool.html', {'name': name, 'loginstatus': loginstatus})


# def news(request):
#
#     return render(request, 'news.html')

def login(request): #登入功能
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
                return HttpResponseRedirect('/home/')
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
        #         return HttpResponseRedirect('/home/')
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

        if check_m:#如果回傳陣列是空的
            status_m = False
        if check_p:#如果回傳陣列是空的
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
            return render_to_response('signin.html', {'status_m': status_m, 'status_p': status_p, 'status_check-password': status_check_password, 'name': name, 'mail': email, 'password': password, 'tel': phone} )

    return render_to_response('signin.html', {'status_m': status_m, 'status_p': status_p, 'status_check_password': status_check_password})


def getpassword(request):
    if request.method == 'POST':
        mail = request.POST.get('mail', '')
        check_mail = RobotMember.objects.filter(email=mail)

        if check_mail is not None:
            new_password = random.randint(10000, 100000)
            new_password = str(new_password)
            send_mail('Your New Password', new_password, 'kfjet123@gmail.com', [mail,], fail_silently=False)
            check_mail.update(password=new_password)
            return render_to_response('login.html')
        else:
            status_m = False
            return render_to_response('forgot.html', {'warn': status_m})

    return render_to_response('forgot.html')

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




def get_news(request): #check
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

    return render_to_response('news.html', {'breaking_news': result, 'global': result_2, 'hot': result_3, 't_all':result_4, 'stock':result_5, 'tec':result_6, 'tra':result_7, 'name': name, 'loginstatus': loginstatus})



def outcome_news(request):#搜尋文章結果 check
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
        res = RobotYahooNew.objects.filter(title = result)[0]
        last = RobotYahooNew.objects.last().id
        if res.id is 1:
            status_prev = False
            next_article = RobotYahooNew.objects.get(id = res.id+1)
            return render_to_response('news_con.html', {'status_prev': status_prev, 'status_next': status_next,'next_article': next_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})
        elif res.id is last:
            status_next = False
            prev_article = RobotYahooNew.objects.get(id = res.id-1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,'prev_article': prev_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})
        else:
            next_article = RobotYahooNew.objects.get(id = res.id+1)
            prev_article = RobotYahooNew.objects.get(id = res.id-1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,'prev_article': prev_article, 'next_article': next_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})

    if type is '2':
        category = '國際財經'
        result = request.GET.get('c', 0)
        res = RobotCna.objects.filter(title = result)[0]
        last = RobotCna.objects.last().id
        if res.id is 520:
            status_prev = False
            next_article = RobotCna.objects.get(id = res.id+1)
            return render_to_response('news_con.html', {'status_prev': status_prev, 'status_next': status_next,'next_article': next_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})
        elif res.id is last:
            status_next = False
            prev_article = RobotCna.objects.get(id = res.id-1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,'prev_article': prev_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})
        else:
            next_article = RobotCna.objects.get(id = res.id+1)
            prev_article = RobotCna.objects.get(id = res.id-1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,'prev_article': prev_article, 'next_article': next_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})

    if type is '3':
        category = '熱門點閱'
        result = request.GET.get('c', 0)
        res = RobotYahooHot.objects.filter(title = result)[0]
        last = RobotYahooHot.objects.last().id
        if res.id is 1:
            status_prev = False
            next_article = RobotYahooHot.objects.get(id = res.id+1)
            return render_to_response('news_con.html', {'status_prev': status_prev, 'status_next': status_next,'next_article': next_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})
        elif res.id is last:
            status_next = False
            prev_article = RobotYahooHot.objects.get(id = res.id-1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,'prev_article': prev_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})
        else:
            next_article = RobotYahooHot.objects.get(id = res.id+1)
            prev_article = RobotYahooHot.objects.get(id = res.id-1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,'prev_article': prev_article, 'next_article': next_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})

    if type is '4':
        category = '台股盤勢'
        result = request.GET.get('c', 0)
        res = RobotYahoo.objects.filter(title = result)[0]
        last = RobotYahoo.objects.last().id
        if res.id is 1:
            status_prev = False
            next_article = RobotYahoo.objects.get(id = res.id+1)
            return render_to_response('news_con.html', {'status_prev': status_prev, 'status_next': status_next,'next_article': next_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})
        elif res.id is last:
            status_next = False
            prev_article = RobotYahoo.objects.get(id = res.id-1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,'prev_article': prev_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})
        else:
            next_article = RobotYahoo.objects.get(id = res.id+1)
            prev_article = RobotYahoo.objects.get(id = res.id-1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,'prev_article': prev_article, 'next_article': next_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})

    if type is '5':
        category = '個股動態'
        result = request.GET.get('c', 0)
        res = RobotYahooStock.objects.filter(title = result)[0]
        last = RobotYahooStock.objects.last().id
        if res.id is 1:
            status_prev = False
            next_article = RobotYahooStock.objects.get(id = res.id+1)
            return render_to_response('news_con.html', {'status_prev': status_prev, 'status_next': status_next,'next_article': next_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})
        elif res.id is last:
            status_next = False
            prev_article = RobotYahooStock.objects.get(id = res.id-1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,'prev_article': prev_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})
        else:
            next_article = RobotYahooStock.objects.get(id = res.id+1)
            prev_article = RobotYahooStock.objects.get(id = res.id-1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,'prev_article': prev_article, 'next_article': next_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})

    if type is '6':
        category = '科技產業'
        result = request.GET.get('c', 0)
        res = RobotYahooTec.objects.filter(title = result)[0]
        last = RobotYahooTec.objects.last().id
        if res.id is 1:
            status_prev = False
            next_article = RobotYahooTec.objects.get(id = res.id+1)
            return render_to_response('news_con.html', {'status_prev': status_prev, 'status_next': status_next,'next_article': next_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})
        elif res.id is last:
            status_next = False
            prev_article = RobotYahooTec.objects.get(id = res.id-1)
            return render_to_response('news_con.html', {'status_next': status_next, 'satus_prev': status_prev,'prev_article': prev_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})
        else:
            next_article = RobotYahooTec.objects.get(id = res.id+1)
            prev_article = RobotYahooTec.objects.get(id = res.id-1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,'prev_article': prev_article, 'next_article': next_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})

    if type is '7':
        category = '傳統產業'
        result = request.GET.get('c', 0)
        res = RobotYahooTra.objects.filter(title = result)[0]
        last = RobotYahooTra.objects.last().id
        if res.id is 1:
            status_prev = False
            next_article = RobotYahooTra.objects.get(id = res.id+1)
            return render_to_response('news_con.html', {'status_prev': status_prev, 'status_next': status_next,'next_article': next_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})
        elif res.id is last:
            status_next = False
            prev_article = RobotYahooTra.objects.get(id = res.id-1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,'prev_article': prev_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})
        else:
            next_article = RobotYahooTra.objects.get(id = res.id+1)
            prev_article = RobotYahooTra.objects.get(id = res.id-1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,'prev_article': prev_article, 'next_article': next_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})

    if type is '8':
        category = '國際財經'
        result = request.GET.get('c', 0)
        res = RobotCna.objects.objects.filter(title = result)[0]
        last = RobotCna.objects.last().id
        if res.id is 1:
            status_prev = False
            next_article = RobotCna.objects.get(id = res.id+1)
            return render_to_response('news_con.html', {'status_prev': status_prev, 'status_next': status_next,'next_article': next_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})
        elif res.id is last:
            status_next = False
            prev_article = RobotCna.objects.get(id = res.id-1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,'prev_article': prev_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})
        else:
            next_article = RobotCna.objects.get(id = res.id+1)
            prev_article = RobotCna.objects.get(id = res.id-1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,'prev_article': prev_article, 'next_article': next_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})

    if type is '9':
        category = '熱門關鍵字'
        result = request.GET.get('c', 0)
        res = RobotYahooTendency.objects.filter(title = result)[0]
        last = RobotYahooTendency.objects.last().id
        if res.id is 1:
            status_prev = False
            next_article = RobotYahooTendency.objects.get(id = res.id+1)
            return render_to_response('news_con.html', {'status_prev': status_prev, 'status_next': status_next,'next_article': next_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})
        elif res.id is last:# 目前只有12筆 之後會增加到30多筆
            status_next = False
            prev_article = RobotYahooTendency.objects.get(id = res.id-1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,'prev_article': prev_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})
        else:
            next_article = RobotYahooTendency.objects.get(id = res.id+1)
            prev_article = RobotYahooTendency.objects.get(id = res.id-1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,'prev_article': prev_article, 'next_article': next_article, 'category': category, 'id': type, 'result': res, 'name': name, 'loginstatus': loginstatus})

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
        list_name = RobotTrackStock.objects.filter(member_id=member_id).order_by('list_name').values('list_name').distinct()
        list2_name = []
        try:
            list2_name = list_name.exclude(list_name=RobotTrackStock.objects.filter(member_id=member_id).order_by('list_name').values('list_name').distinct().first()['list_name'])
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
            s = Share(i.stock_id+'.TW')
            s1,s2, s3, s4 = s.get_price(),s.get_change(),s.get_percent_change(),s.get_volume()
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
            info.append({'list_name':i.list_name,'stock_id':i.stock_id, 'stock_name':i.stock_name,'price':s1,'change':s2,'change_percent':s3,'vol':s4,'capital':capital,'industry':indusry_name})
        return render_to_response('home.html', {'loginstatus': loginstatus, 'name': name, 'res':res, 'res_3':res_3,'rank':rank,
                                                'rank2':rank2,'hot':hot,'rank3':rank3,'rank4':rank4,'rank_name':rank_stock_name,
                                                'rank2_name':rank2_stock_name,'rank3_name':rank3_stock_name,'rank4_name':rank4_stock_name,
                                                'list_name':list_name,'list2_name': list2_name, 'track':info})
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
        return render_to_response('home.html', {'loginstatus': loginstatus, 'name': name, 'res':res, 'res_3':res_3,'rank':rank,
                                                'rank2':rank2,'hot':hot,'rank3':rank3,'rank4':rank4,'rank_name':rank_stock_name,
                                                'rank2_name':rank2_stock_name,'rank3_name':rank3_stock_name,'rank4_name':rank4_stock_name,
                                                })






#
# def trade(request):
#    name = ''
#    loginstatus = False
#    try:
#         name = request.session['name']
#         loginstatus = True
#    except:
#         return HttpResponseRedirect('/login/?back=模擬交易所')
#    type = request.GET.get('type', '')
#    if type == 'multichart':
#         os.system('D:\Multichart64\MultiCharts64.exe')
#         return render_to_response('financial.html', {'loginstatus': loginstatus, 'name': name})
#    elif type == 'pyalgotrade':
#         pass
#         return render_to_response('', {'loginstatus': loginstatus, 'name': name})
#    else:
#         return render_to_response('financial.html', {'loginstatus': loginstatus, 'name': name})
#
# #
# def register(request):
#     if request.method == 'POST':
#         form= UserCreationForm(request.Post)
#         if form.is_valid():
#             form.save()
#             username=form.cleaned_data.get('username')
#             messages.success(request, f'Account creadted for {username}!')
#             return redirect('login')
#     else:
#         form =UserCreationForm()
#     return render(request,'register.html',{'form':form})