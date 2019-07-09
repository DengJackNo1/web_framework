from project.settings import TEMPLATES_DIRS, STATICFILES_DIRS, BASE_DIR
import os


class Response:

    def __init__(self, request, encoding="utf-8", status=200, status_content="OK"):
        self.request = request
        self.encoding = encoding
        self.lst = []
        self.status = status
        self.status_content = status_content
        self.content_type = 'Content-Type: {}'
        self.server = 'Server: WSGIServer/0.2 CPython/3.6.8'
        self.content_length = 'Content-Length: {}'
        self.X_Frame_Options = 'X-Frame-Options: SAMEORIGIN'

    def process_response_first_line(self):
        self.response_first = self.request.HTTP + ' ' + str(self.status) + ' ' + self.status_content
        self.lst.append(self.response_first)
        self.lst.extend([self.content_type, self.content_length, self.server])

    def try_read_file(self, file_name, DIRS):
        for dir in DIRS:
            file_path = os.path.join(dir, file_name)
            try:
                with open(file_path, 'rb') as f:
                    self.content = f.read()
                    self.content_length = 'Content-Length: {}'.format(len(self.content))
                    self.process_response_first_line()
                    self.lst.append(self.X_Frame_Options)
                    break
            except FileNotFoundError:
                pass
        else:
            self.content_length = 'Content-Length: {}'.format(0)
            self.content = b'0'
            self.obj = Http404(self.request)


class HttpResponse(Response):
    def __init__(self, text, *args, **kwargs, ):
        super(HttpResponse, self).__init__(*args, **kwargs)
        self.content_type = self.content_type.format('text/html; charset={}'.format(self.encoding))
        self.content = text.encode(self.encoding)
        self.content_length = 'Content-Length: {}'.format(len(self.content))
        self.process_response_first_line()
        self.lst.extend([self.X_Frame_Options])

    def __call__(self, *args, **kwargs):
        ret = ('\r\n'.join(self.lst) + '\r\n\r\n').encode(self.encoding)
        ret += self.content
        return ret


class Render(Response):
    def __init__(self, template_name, *args, **kwargs, ):
        super(Render, self).__init__(*args, **kwargs)
        self.content_type = self.content_type.format('text/html; charset={}'.format(self.encoding))
        self.try_read_file(template_name, TEMPLATES_DIRS)

    def __call__(self, *args, **kwargs):
        ret = '\r\n'.join(self.lst)
        if self.content != b'0':
            ret = ret.encode(self.encoding) + '\r\n\r\n'.encode(self.encoding) + self.content
            return ret
        else:
            return self.obj()


class Redirect(Response):
    """HTTP/1.0 302 Found
Date: Fri, 05 Jul 2019 11:47:35 GMT
Server: WSGIServer/0.2 CPython/3.6.8
Content-Type: text/html; charset=utf-8
Location: /crm/customer_list/
X-Frame-Options: SAMEORIGIN
Content-Length: 0"""

    def __init__(self, to, *args, **kwargs, ):
        super(Redirect, self).__init__(*args, **kwargs)
        self.status = 302
        self.status_content = 'Found'
        self.content_type = self.content_type.format('text/html; charset={}'.format(self.encoding))
        self.content_length = 'Content-Length: 0'
        self.Location = 'Location: {}'.format(to)
        self.process_response_first_line()
        self.lst.extend([self.Location, self.X_Frame_Options, ])

    def __call__(self, *args, **kwargs):
        ret = '\r\n'.join(self.lst) + '\r\n\r\n'
        ret = ret.encode(self.encoding)
        return ret


class Http404(Response):
    def __init__(self, *args, **kwargs, ):
        super(Http404, self).__init__(*args, **kwargs)
        self.status = 404
        self.status_content = 'Not Found'
        self.content_type = self.content_type.format('text/html; charset={}'.format(self.encoding))
        self.content_length = 'Content-Length: 0'
        self.try_read_file('http404.html', TEMPLATES_DIRS)

    def __call__(self, *args, **kwargs):
        ret = ('\r\n'.join(self.lst) + '\r\n\r\n').encode(self.encoding) + self.content
        return ret


class StaticFileResponse(Response):
    def __init__(self, static_file_name, *args, **kwargs, ):
        super(StaticFileResponse, self).__init__(*args, **kwargs)
        file_last = static_file_name.rsplit('.', 1)[-1].lower()
        info = {'css': 'text/css', 'js': 'application/javascript', 'png': 'image/png',
                'svg': 'image/svg+xml', 'jpg': 'image/jpeg', 'jpeg': 'image/jpeg', 'ico': 'image/x-icon'}
        self.content_type = self.content_type.format(info.get(file_last, 'text/html; charset={}'.format(self.encoding)))
        if static_file_name == 'favicon.ico':
            self.try_read_file(static_file_name, [BASE_DIR, ])
        else:
            self.try_read_file(static_file_name, STATICFILES_DIRS)

    def __call__(self, *args, **kwargs):
        ret = '\r\n'.join(self.lst)
        if self.content != b"0":
            ret = ret.encode(self.encoding) + '\r\n\r\n'.encode(self.encoding) + self.content
            return ret
        else:
            return self.obj()
