class HttpRequest(object):

    def __init__(self, response):
        # print('浏览器发送过来的请求数据', response)
        data = response.split('\r\n')
        # print(data)
        self.FirstLine = data[0]
        self.body = data[1:]
        self.method = self.FirstLine.split(" ")[0]
        # 带url 和 参数 ,不带端口
        self.full_path = self.FirstLine.split(" ")[1]
        self.GET = self.full_path.rsplit('?', 1)[-1]
        self.path = self.full_path.split("?")[0]
        # HTTP及版本号
        self.HTTP = self.FirstLine.split(" ")[2]
        self.HOST = data[1].split(" ")[-1].split(":")[0]
        self.PORT = data[1].split(" ")[-1].split(":")[1]

        self.POST = data[-1]
        self.body = data[1:]
        self.META = self.body[:-2]
        self.GET = self.__dic_from_str(self.GET)
        self.POST = self.__dic_from_str(self.POST)
        self.__process_meta()
        self.COOKIES = self.META.get('Cookie', None)
        if self.COOKIES:
            self.COOKIES = self.__dic_from_str(self.COOKIES, seq=";")

    def __dic_from_str(self, content, seq="&"):
        try:
            lst = content.split(seq)
            dic = {}
            for item in lst:
                a, b = item.strip().split('=', 1)
                dic.update({a: b})
            ret = dic
        except AttributeError:
            ret = {}
        except ValueError:
            ret = {}
        return ret

    def __process_meta(self):
        dic = {}
        for item in self.META:
            a, b = item.split(':', 1)
            dic.update({a: b})
        self.META = dic
