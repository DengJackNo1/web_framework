from MyWeb_framework.core.Urls import Url
# 导入自己的app的视图函数
from myapp import views

urlpatterns = [
    Url(r'^index/$', views.index),
    Url(r'^login/$', views.Login.as_view()),
    Url(r'^reg/$', views.reg),
]
