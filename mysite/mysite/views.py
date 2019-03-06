from django.shortcuts import render,render_to_response,HttpResponseRedirect

from .models import Member

def home(request):
    #return HttpResponse('about')
    return render(request, 'home.html')

def login(request): #登入功能
    status_m = False
    status_p = False
    back = request.GET.get('back', 0)
    article_id = request.GET.get('article_id', 0)
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        check_m = Member.objects.filter(email__exact=username)
        check_p = Member.objects.filter(password__exact=password)

        if check_m is not None:
            status_m = True
        if check_p is not None:
            status_p = True

        user = Member.objects.filter(email=username, password=password)

        if user and status_m is True and status_p is True:
            request.session['userName'] = user[0].email
            request.session['password'] = user[0].password
            request.session['name'] = user[0].member_name
            if back == '0' or back == '':
                return HttpResponseRedirect('/home/')
            elif back == '討論區發文':
                return HttpResponseRedirect('/post/')
            elif back == '討論區回覆':
                return HttpResponseRedirect('/chat_outcome/?id='+article_id)
            elif back == '未來型預測':
                return HttpResponseRedirect('/predict/')
            elif back == '修改基本資料':
                return HttpResponseRedirect('/modify/')
            elif back == '修改密碼':
                return HttpResponseRedirect('/mo_pass/')
            elif back == '新聞首頁':
                return HttpResponseRedirect('/get_news/')
            elif back == '系統首頁':
                return HttpResponseRedirect('/home/')
            elif back == 'My_News':
                return HttpResponseRedirect('/member_news/')
        else:
            return render_to_response('login.html', {'status_m': status_m, 'status_p': status_p})

    return render_to_response('login.html', {'back': back, 'article_id': article_id})
