import os
from MyWeb_framework.conf import settings
from .httpresponse import Http3xxResponse, Http2xxResponse, Http404Response


class HttpResponseBase(object):

    def __init__(self, request=None, encoding="utf-8"):
        self.request = request
        self.HTTP = request.HTTP if request else 'HTTP/1.1'
        self.lst = []
        self.encoding = encoding
        self.type = 'text/html; charset={}'.format(self.encoding)
        self.content_type = 'Content-Type: {}'.format(self.type)
        self.content_length = 'Content-Length: {}'
        self.server = 'Server: WSGIServer/0.2 CPython/3.6.8'
        self.X_Frame_Options = 'X-Frame-Options: SAMEORIGIN'

    def process_response_first_line(self):
        self.response_first = self.HTTP + ' ' + \
                              str(self.status_code) + ' ' + self.status_content
        self.lst.append(self.response_first)
        self.lst.extend([self.content_type, self.content_length, self.server])

    def try_read_file(self, file_name, DIRS):
        for dir in DIRS:
            file_path = os.path.join(dir, file_name)
            try:
                with open(file_path, 'rb') as f:
                    self.content = f.read()
                    self.content_length = 'Content-Length: {}'.format(
                        len(self.content))
                    self.process_response_first_line()
                    self.lst.append(self.X_Frame_Options)
                    break
            except FileNotFoundError:
                pass
        else:
            self.content_length = 'Content-Length: {}'.format(0)
            self.content = None

    def _object(self):
        if self.content:
            return self
        return Http404(self.request)

    def __call__(self, *args, **kwargs):
        ret = ('\r\n'.join(self.lst) + '\r\n\r\n').encode(self.encoding)
        return ret + self.content

    def set_cookies(self, key, value, max_age=1209600, path='/', HttpOnly=True):
        if HttpOnly:
            HttpOnly = ' HttpOnly;'
        else:
            HttpOnly = ''
        Max_Age = 'Max-Age=%s;' % max_age
        Path = 'Path=%s;' % path
        self.Cookies = 'Set-Cookie:  %(key)s=%(value)s;%(HttpOnly)s %(Max-Age)s %(Path)s' \
                       % {'key': key, 'value': value, 'HttpOnly': HttpOnly, 'Max-Age': Max_Age,
                          'Path': Path}
        self.lst.append(self.Cookies)

    def __setitem__(self, key, value):
        setattr(self, key, '%s: %s' % (key, value))
        self.lst.append(getattr(self, key, default=None))


class HttpResponse(HttpResponseBase, Http2xxResponse):
    def __init__(self, text, *args, **kwargs, ):
        super().__init__(*args, **kwargs)
        self.content = text.encode(self.encoding)
        self.content_length = 'Content-Length: {}'.format(len(self.content))
        self.process_response_first_line()
        self.lst.extend([self.X_Frame_Options])


class render(HttpResponseBase, Http2xxResponse):
    def __init__(self, request, template_name, *args, **kwargs, ):
        super().__init__(request, *args, **kwargs)
        self.try_read_file(template_name, settings.TEMPLATES_DIRS)


class redirect(HttpResponseBase, Http3xxResponse):
    """HTTP/1.0 302 Found
Date: Fri, 05 Jul 2019 11:47:35 GMT
Server: WSGIServer/0.2 CPython/3.6.8
Content-Type: text/html; charset=utf-8
Location: /crm/customer_list/
X-Frame-Options: SAMEORIGIN
Content-Length: 0"""

    def __init__(self, to, *args, **kwargs, ):
        super().__init__(*args, **kwargs)
        self.content_length = 'Content-Length: 0'
        self.Location = 'Location: {}'.format(to)
        self.process_response_first_line()
        self.lst.extend([self.Location, self.X_Frame_Options, ])
        self.content = b'0'


class Http404(HttpResponseBase, Http404Response):
    def __init__(self, *args, **kwargs, ):
        super().__init__(*args, **kwargs)
        self.type = 'text/html; charset={}'.format(self.encoding)
        self.content_length = 'Content-Length: 0'
        self.try_read_file('http404.html', settings.TEMPLATES_DIRS)

    def __call__(self, *args, **kwargs):
        ret = ('\r\n'.join(self.lst) + '\r\n\r\n').encode(self.encoding)
        return ret + self.content


class StaticFileResponse(HttpResponseBase, Http2xxResponse):
    def __init__(self, static_file_name, *args, **kwargs, ):
        super().__init__(*args, **kwargs)
        file_last = static_file_name.rsplit('.', 1)[-1].lower()
        info = {'css': 'text/css', 'js': 'application/javascript', 'png': 'image/png', 'svg': 'image/svg+xml',
                'jpg': 'image/jpeg', 'jpeg': 'image/jpeg', 'ico': 'image/x-icon'}
        self.type = info.get(file_last, 'text/html; charset={}'.format(self.encoding))
        self.content_type = 'Content-Type: {}'.format(self.type)
        if static_file_name == 'favicon.ico':
            self.try_read_file(static_file_name, [settings.BASE_DIR, ])
        else:
            self.try_read_file(static_file_name, settings.STATICFILES_DIRS)
