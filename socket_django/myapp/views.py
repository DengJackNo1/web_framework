from MyWeb_framework.core.http import render, redirect
from MyWeb_framework.view.view import View


# 在这里写你的视图函数

def index(request):
    return render(request, 'index.html')


def reg(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        return redirect(to='/login/')
    return render(request, 'reg.html')


def login(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        if user == 'alex' and pwd == '123':
            return redirect(to='/index/')
    return render(request, 'login.html')


class Login(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')

    def post(self, request):
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        if user == 'alex' and pwd == '123':
            return redirect(to='/index/')
        return render(request, 'login.html')
