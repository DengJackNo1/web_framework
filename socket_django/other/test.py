def one():
    import re
    import os

    url = 'http://127.0.0.1:65530/reg/1/'
    url1 = 'reg/1/3/'
    lst = [r'^index/$', r'^login/$', r'^reg/((?P<name>\d+)/$']

    # for i in lst:
    #     if re.match(i,url1):
    #         ret = re.match(i,url1)
    #         print(ret.groupdict(),ret.groups())

    path = os.path.dirname(__file__)
    for a, b, c in os.walk(path):
        for file in c:
            ppp = os.path.join(a, file)
            if ppp.endswith('.py'):
                os.system(
                    'autopep8 --in-place --aggressive --aggressive {}'.format(ppp))


class te(object):

    def __setitem__(self, key, value):
        print(key, value)
        return setattr(self, key, value)

    def __getitem__(self, item):
        return getattr(self,item,None)




import web

urls = (
    '/(.*)', 'hello'
)
app = web.application(urls, globals())

class hello:
    def GET(self, name):
        if not name:
            name = 'World'
        return 'Hello, ' + name + '!'

if __name__ == "__main__":
    app.run()
