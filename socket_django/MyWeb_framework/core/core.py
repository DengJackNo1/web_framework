import re
from MyWeb_framework.conf import settings
from MyWeb_framework.core.http import HttpRequest, redirect, Http404
from .middle_core import Middle_Process
import importlib
urls = importlib.import_module(settings.ROOT_URLCONF)


def first_process_res(recv, encoding="UTF-8"):
    """
    :param recv: socket服务端从浏览器接收到的请求,字节型数据
    :return:
    """
    # ,最先开始处理
    return HttpRequest(recv.decode(encoding))


def re_urlpatterns_view(request):
    """在url视图之前调用,并调用视图函数,
    或者直接返回重定向"""
    path = request.path.lstrip('/')
    for url in urls.urlpatterns:
        if re.search(url.re_path, path):
            ret = re.search(url.re_path, path)
            args_list = list(ret.groups())
            for value in ret.groupdict().values():
                args_list.remove(value)

            # 视图函数执行,返回返回值
            return url.handler(request, *args_list, **ret.groupdict(), )
        else:
            if re.search(url.re_path, path + '/'):
                request.path += '/'
                return redirect(request.path, request)
    else:
        return Http404(request)


def request_response(recv):
    request = first_process_res(recv)

    # 先执行中间件的process_request方法
    response = Middle_Process._full_middle_process_request(request)
    if response:
        # 默认process_request返回的是None,若返回response对象(),直接返回给浏览器
        return Middle_Process._full_middle_process_response(request, response)
    # 再执行中间件的process_view方法,在视图函数之前执行
    response = Middle_Process._full_middle_process_view(request)
    if response:
        # 默认process_request返回的是None,若返回response对象(),直接返回给浏览器
        return Middle_Process._full_middle_process_response(request, response)

    # 执行视图函数, 通过url的正则匹配, 执行对应的视图函数
    response = re_urlpatterns_view(request)
    #  再执行中间件的process_response方法,在视图函数之前执行
    response = Middle_Process._full_middle_process_response(request, response)
    # response = Middle_Process._full_middle_process_response(request, response)
    # 执行中间件的process_request方法

    return response
