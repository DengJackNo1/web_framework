import os

if __name__ == '__main__':
    try:
        os.environ.setdefault('WyWeb_framework_setting', '%(project_name)s.settings')
    except Exception as  e:
        print(e)

    from MyWeb_framework.wsgi_socket.socket_serverWSGI import server_begin

    server_begin()
