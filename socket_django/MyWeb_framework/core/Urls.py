class Url:
    def __init__(self, path, handler, name=None, params=None):
        """
        :param path:url路径
        :param handler:url对应的视图函数
        :param name:反向解析的name
        :param params: {},存放参数
        """
        self.re_path = path
        self.handler = handler
        self.name = name
        self.params = params
