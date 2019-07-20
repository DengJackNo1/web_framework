class View(object):
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']

    @classmethod
    def as_view(cls, *args, **kwargs):
        self = cls()
        return self.view

    def view(self, request, *args, **kwargs):
        self.request = request
        return self.dispatch(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower())
        else:
            handler = self.http_method_not_allowed
        print(handler)
        return handler(request, *args, **kwargs)

    def http_method_not_allowed(self, request, *args, **kwargs):
        pass