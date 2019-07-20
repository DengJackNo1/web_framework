import os
import sys

if __name__ == '__main__':
    try:
        os.environ.setdefault('WyWeb_framework_setting', 'oldboy.settings')
    except Exception as  e:
        print(e)

    from MyWeb_framework.wsgi_socket.socket_serverWSGI import runserver
    runserver(sys.argv)
