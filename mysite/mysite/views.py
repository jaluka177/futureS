from django.shortcuts import render,render_to_response,HttpResponseRedirect

def home(request):
    #return HttpResponse('about')
    return render(request, 'home.html')