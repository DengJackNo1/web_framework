from MyWeb_framework.core.response import  HttpResponse

# 在这里写你的视图函数

def index(request):
    return HttpResponse("首页", request)

