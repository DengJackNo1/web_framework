import socketserver
from MyWeb_framework.conf import settings


from MyWeb_framework.logger.logger import logger
from MyWeb_framework.core.core import request_response




class MyServer(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            ret = self.request.recv(1500)
            # 一次TCP最大发送长度为1500
            if ret:
                response = request_response(ret)
                self.request.send(response._object()())


def runserver(*args):
    try:
        if len(args) == 1:
            settings.PORT = int(args[0])
        elif len(args) == 2:
            settings.HOST = int(args[0])
            settings.PORT = int(args[0])
        server = socketserver.ThreadingTCPServer(((settings.HOST, settings.PORT)), MyServer)
        logger.error('runserver:%s:%s\nwelcome use my webframework' % (settings.HOST, settings.PORT,))
        server.serve_forever()
    except KeyboardInterrupt:
        exit()
