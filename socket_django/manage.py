import os
import sys

if __name__ == '__main__':
    try:
        os.environ.setdefault('WyWeb_framework_setting', 'project.settings')
    except Exception as  e:
        print(e)
    from MyWeb_framework.wsgi_socket.socket_serverWSGI import runserver
    lst = sys.argv[1:]
    try:
        if not lst:
            raise Exception('输入错误')
        elif hasattr(sys.modules[__name__], lst[0]):
            if len(lst) == 2:
                getattr(sys.modules[__name__], lst[0])(*lst[1:])
    except Exception:
        exit(0)
