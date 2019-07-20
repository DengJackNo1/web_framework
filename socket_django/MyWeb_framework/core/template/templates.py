from jinja2 import FileSystemLoader, Environment, Template
from project.settings import TEMPLATES_DIRS


def read_html(file, request):
    with open(file, "r", encoding="utf8") as f:
        data = f.read()
        template = Template(data)  # 生成模板文件
        ret = template.render({'request': request})  # 把数据填充到模板中
    return ret


loader = FileSystemLoader(searchpath=TEMPLATES_DIRS[0])
env = Environment(loader=loader)
template = env.get_template('http404.html')
print(template.render({'name':{'tt':'等一下你'}}))
