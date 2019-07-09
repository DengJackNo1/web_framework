from project.settings import HOST, PORT
from MyWeb_framework.logger.logger import logger
import socketserver
from MyWeb_framework.core.middle_core import request_response

logger.error('runserver:%s:%s' % (HOST, PORT))


class MyServer(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            ret = self.request.recv(1500)
            # 一次TCP最大发送长度为1500
            response = request_response(ret)
            self.request.send(response())


server = socketserver.ThreadingTCPServer(((HOST, PORT)), MyServer)
server_begin = server.serve_forever
