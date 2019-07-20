import importlib
from MyWeb_framework.conf import settings

class Middle_Process:
    # 请求到来时,先执行中间件方法

    @staticmethod
    def _full_middle_process_request(request):
        request.index = 0
        # 记录Index,记录执行到那个中间件的process_request方法了,直接倒序执行对应的process_response方法
        for mid_ware in settings.MIDDLE_WARES:
            module_name, classname = mid_ware.rsplit('.', 1)
            val = importlib.import_module(module_name)
            request.index += 1
            module_getattr = getattr(val, classname)
            ret = (getattr(module_getattr(), 'process_request'))(request)
            if ret:  # 有返回值,不为空,response
                return ret

    @staticmethod
    def _full_middle_process_view(request):
        for mid_ware in settings.MIDDLE_WARES:
            module_name, classname = mid_ware.rsplit('.', 1)
            val = importlib.import_module(module_name)
            module_getattr = getattr(val, classname)
            ret = (getattr(module_getattr(), 'process_view'))(request)
            if ret:  # 有返回值,不为空,特殊
                return ret

    @staticmethod
    def _full_middle_process_response(request, response, ):
        for mid_ware in settings.MIDDLE_WARES[request.index::-1]:
            # 倒序执行
            module_name, classname = mid_ware.rsplit('.', 1)
            # a 是 模块名(py文件) , b是类名
            val = importlib.import_module(module_name)
            module_getattr = getattr(val, classname)
            response = (getattr(module_getattr(),'process_response'))(request,response)
        return response