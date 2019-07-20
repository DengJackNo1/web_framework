import os

HOST = '127.0.0.1'
PORT = 65530
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMPLATES_URL = "/templates/"
TEMPLATES_DIRS = [os.path.join(BASE_DIR, "templates"), ]

STATICS_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]

ROOT_URLCONF = '%(project_name)s.urls'

# 定义中间件
MIDDLE_WARES = [
    'MyWeb_framework.middlewares.middlewares.LoggerMiddleWares',
    # 中间件类(记录日志用)
    'MyWeb_framework.middlewares.middlewares.FaviconMiddleWares',
    # 中间件类(处理网站的根目录的favicon.ico图标)
    'MyWeb_framework.middlewares.middlewares.AdminMiddleWares',
    # 中间件类(处理静态文件-->/static/,直接返回文件)
]

OMIT_URLS = True
