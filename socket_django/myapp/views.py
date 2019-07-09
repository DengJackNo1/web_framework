from MyWeb_framework.core.response import Render, HttpResponse ,Redirect

# 在这里写你的视图函数

def index(request):
    return Render("login.html", request)


def login(request):
    return Render("login.html", request)


def reg(request):
    return HttpResponse('OKOKOKOK', request)
