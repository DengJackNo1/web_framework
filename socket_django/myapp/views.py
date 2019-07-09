from MyWeb_framework.core.response import Render, HttpResponse, Redirect, Http404


# 在这里写你的视图函数

def index(request):
    ret = Render("login.html", request)
    request.name = '我的名字'
    return ret


def login(request):
    print('login')
    return Redirect('/index/', request)


def reg(request):
    request.hh = '123456'
    return Http404(request)
