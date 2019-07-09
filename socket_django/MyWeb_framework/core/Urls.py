
class Url:
    def __init__(self, path, handler, name=None, **kwargs):
        self.re_path = path
        self.handler = handler
        self.name = name
        self.kwargs = kwargs



