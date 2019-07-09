from MyWeb_framework.core.response import StaticFileResponse
from MyWeb_framework.logger.logger import logger


class MiddleBase:

    def process_request(self, request):
        pass

    def process_view(self, request):
        pass

    def process_response(self, request, response):
        return response


class AdminMiddleWares(MiddleBase):
    def process_request(self, request):
        # 在视图处理函数之前执行
        if request.path.startswith('/static/'):
            file_name = request.path.lstrip('/static/')
            return StaticFileResponse(file_name, request)


class FaviconMiddleWares(MiddleBase):
    def process_request(self, request):
        # 在视图处理函数之前执行
        if request.path.startswith('/favicon.ico'):
            return StaticFileResponse('favicon.ico', request)


class LoggerMiddleWares(MiddleBase):
    def process_response(self, request, response):
        logger.error(
            "'%s %s' %s %s" % (
                request.method, request.full_path, response.status, response.status_content,))
        return response

