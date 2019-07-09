#!/usr/bin/env python
# -*- coding:utf-8 -*-

class Request(object):

    def __init__(self, response):
        data = response.split('\r\n')
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

        self.__dic_from_str(self.GET)
        self.__dic_from_str(self.POST)
        self.__process_meta()

    def __dic_from_str(self, content):
        try:
            lst = content.split("&")
            dic = {}
            for item in lst:
                a, b = item.split('=', 1)
                dic.update({a: b})
            content = dic
        except AttributeError:
            content = {}
        except ValueError:
            content = {}

    def __process_meta(self):
        dic = {}
        for item in self.META:
            a, b = item.split(':', 1)
            dic.update({a: b})
        self.META = dic
