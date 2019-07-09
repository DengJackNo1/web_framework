from project.settings import MIDDLE_WARES
from MyWeb_framework.core.request import Request
import importlib
from project.urls import urlpatterns
import re
from MyWeb_framework.core.response import Http404, Redirect
from project.settings import OMIT_URLS


class Middle_Process:
    # 请求到来时,先执行中间件方法

    @staticmethod
    def _full_middle_process_request(request):
        request.index = 0
        # 记录Index,记录执行到那个中间件的process_request方法了,直接倒序执行对应的process_response方法
        for mid_ware in MIDDLE_WARES:
            module_name, classname = mid_ware.rsplit('.', 1)
            val = importlib.import_module(module_name)
            request.index += 1
            module_getattr = getattr(val, classname)
            ret = (getattr(module_getattr(), 'process_request'))(request)
            if ret:  # 有返回值,不为空,response
                return ret

    @staticmethod
    def _full_middle_process_view(request):
        for mid_ware in MIDDLE_WARES:
            module_name, classname = mid_ware.rsplit('.', 1)
            val = importlib.import_module(module_name)
            module_getattr = getattr(val, classname)
            ret = (getattr(module_getattr(), 'process_view'))(request)
            if ret:  # 有返回值,不为空,正常流程
                return ret

    @staticmethod
    def _full_middle_process_response(request, response, ):
        for mid_ware in MIDDLE_WARES[request.index::-1]:
            # 倒序执行
            module_name, classname = mid_ware.rsplit('.', 1)
            # a 是 模块名(py文件) , b是类名
            val = importlib.import_module(module_name)
            module_getattr = getattr(val, classname)
            response = (getattr(module_getattr(), 'process_response'))(request, response)
        return response


def first_process_res(recv, encoding="UTF-8"):
    """

    :param recv: socket服务端从浏览器接收到的请求,字节型数据
    :return:
    """
    # ,最先开始处理
    return Request(recv.decode(encoding))


def re_urlpatterns_view(request):
    """在url视图之前调用,并调用视图函数,
    或者直接返回重定向"""
    path = request.path.lstrip('/')
    for url in urlpatterns:
        if re.search(url.re_path, path):
            return url.handler(request)
        else:
            if re.search(url.re_path, path + '/'):
                request.path += '/'
                return Redirect(request.path, request)


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
