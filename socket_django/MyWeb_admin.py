import sys, os

t = sys.modules['__main__']

lst = sys.argv[1:]
if len(lst) == 0:
    pass
elif len(lst) == 2:
    pass


def startproject(name):
    path = os.getcwd()
    project_path = os.path.join(path, name)
    if not os.path.exists(project_path):
        os.mkdir(project_path)
    oldproject = os.path.join(path, 'MyWeb_framework', 'oldproject')
    for file in os.listdir(oldproject):
        file_path = os.path.join(oldproject, file)
        project_new_path = os.path.join(project_path, file)
        with open(file_path, 'rb') as oldf, open(project_new_path, 'wb') as newf:
            data = oldf.read()
            newf.write(data)


def startapp(name):
    path = os.getcwd()
    app_path = os.path.join(path, name)
    if not os.path.exists(app_path):
        os.mkdir(app_path)
    oldapp = os.path.join(path, 'MyWeb_framework', 'oldapp')
    for file in os.listdir(oldapp):
        file_path = os.path.join(oldapp, file)
        app_new_path = os.path.join(oldapp, file)
        with open(file_path, 'rb') as oldf, open(app_new_path, 'wb') as newf:
            data = oldf.read()
            newf.write(data)
