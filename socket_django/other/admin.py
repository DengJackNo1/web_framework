import sys
import os


def copy_process_file(oldproject, project_path, name):
    if not os.path.exists(project_path):
        os.makedirs(project_path)
    for file in os.listdir(oldproject):
        file_path = os.path.join(oldproject, file)
        project_new_path = os.path.join(project_path, file)
        with open(file_path, 'r', encoding='utf-8') as oldf, open(project_new_path, 'w', encoding='utf-8') as newf:
            data = oldf.read()
            if file in {'settings.py', 'manage.py'}:
                newf.write(data % {'project_name': name})
                continue
            newf.write(data)


def startproject(name):
    path = os.getcwd()
    project_path = os.path.join(path, name)
    input()
    for module_path in sys.path:
        oldproject = os.path.join(module_path, 'MyWeb_framework', 'project', 'oldproject')
        old_manage_path = os.path.join(module_path, 'MyWeb_framework', 'project', 'oldothers')
        print(oldproject)
        print(old_manage_path)
        if os.path.exists(oldproject):
            break
    input()
    copy_process_file(old_manage_path, project_path, name)
    project_path = os.path.join(path, name, name)
    copy_process_file(oldproject, project_path, name)



def test():
    # 运行目录
    CurrentPath = os.getcwd()
    print(CurrentPath, 'os.getcwd()')

    # 当前脚本目录
    print('##################################################')
    print(os.path, 'os.path>>>')

    print(sys.argv[0], 'sys.argv[0]')
    print(sys.path, 'sys.path')

    print(os.path.split(os.path.realpath(sys.argv[0])),
          'os.path.split(os.path.realpath(sys.argv[0])),')
    # exe 文件后的路径 和文件名
    print("##################################################")

    ScriptPath = os.path.split(os.path.realpath(sys.argv[0]))[0]
    print(ScriptPath, 'ScriptPath')

    print('sys.moudles')
    print(sys.modules['__main__'])
    for i in sys.path:
        print(i)

    print(1231321321)
    print(os.path.abspath(__file__))
    print(123144654 + 48)
    print()
    print()

    for i in os.environ['PATH'].split(';'):
        path = os.path.join(i, 'admin.exe')
        if os.path.exists(path):
            print(path)
    input('>>>>>>>>>>>>>>>>>>>>>>>>>>')

def get_module():
    ScriptPath = os.path.split(os.path.realpath(sys.argv[0]))[0]
    dir_path = os.path.dirname(ScriptPath)
    module_path = os.path.join(dir_path, 'Lib', 'site-packages')
    return module_path

if __name__ == '__main__':
    startproject('oldboy')



