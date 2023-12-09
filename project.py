import glob
import json
import os.path
import shutil
import subprocess
import uuid

from util.file import exists_dir, file_name_ext, exists_file
from util.os_info import is_windows, is_x64

PYTHON_WIN64_EXE = [
    'windows-x86_64/python.exe',
    'windows-x86_64/pythonw.exe',
    'py2-windows-x86_64/python.exe',
    'py2-windows-x86_64/pythonw.exe',
    'py3-windows-x86_64/python.exe',
    'py3-windows-x86_64/pythonw.exe',
]
PYTHON_WIN32_EXE = [
    'windows-x86_64/python.exe',
    'windows-x86_64/pythonw.exe',
    'py2-windows-i686/python.exe',
    'py2-windows-i686/pythonw.exe',
    'py3-windows-i686/python.exe',
    'py3-windows-i686/pythonw.exe',
]
PYTHON_LINUX64_EXE = [
    'linux-x86_64/python',
    'linux-x86_64/pythonw',
    'py2-linux-x86_64/python',
    'py2-linux-x86_64/pythonw',
    'py3-linux-x86_64/python',
    'py3-linux-x86_64/pythonw',
]
PYTHON_LINUX32_EXE = [
    'linux-i686/python',
    'linux-i686/pythonw',
    'py2-linux-i686/python',
    'py2-linux-i686/pythonw',
    'py3-linux-i686/python',
    'py3-linux-i686/pythonw',
]
RENPY_DIRS = [
    'game',
    'renpy',
    'lib',
]



def check_renpy_dir(abs_path):
    assert exists_dir(abs_path), f'{abs_path} is not a dir!'
    for d in RENPY_DIRS:
        absd = os.path.join(abs_path, d)
        assert exists_dir(absd), f'The dir({d}) is required in {abs_path}!'

def find_project_name(abs_path):
    py_files = [file_name_ext(f)[0] for f in glob.glob(os.path.join(abs_path, '*.py'))]
    sh_files = [file_name_ext(f)[0] for f in glob.glob(os.path.join(abs_path, '*.sh'))]
    exe_files = [file_name_ext(f)[0] for f in glob.glob(os.path.join(abs_path, '*.exe'))]

    project_name = None
    if is_windows():
        same_name_files = exe_files
    else:
        same_name_files = sh_files

    for py_name in py_files:
        if py_name in same_name_files:
            project_name = py_name
            break
    assert project_name is not None, f'Coundn\'t find a entrypoint file in {abs_path}'
    return project_name
def find_exe(abs_path):
    executable_path = None
    lib_path = os.path.join(abs_path, 'lib')
    if is_x64():
        if is_windows():
            pyexe_files = [os.path.join(lib_path, exe) for exe in PYTHON_WIN64_EXE]
        else:
            pyexe_files = [os.path.join(lib_path, exe) for exe in PYTHON_LINUX64_EXE]
    else:
        if is_windows():
            pyexe_files = [os.path.join(lib_path, exe) for exe in PYTHON_WIN32_EXE]
        else:
            pyexe_files = [os.path.join(lib_path, exe) for exe in PYTHON_LINUX32_EXE]
    for pyexe in pyexe_files:
        if exists_file(pyexe):
            executable_path = pyexe
            break
    assert executable_path is not None, f'Coundn\'t find a executable file file in {lib_path}'
    return executable_path


def do_injection(abs_path):
    renpy_init_py = os.path.join(abs_path, 'renpy', '__init__.py')
    injection_py = os.path.join(abs_path, 'renpy', 'translation', 'projz_inject.py')
    if exists_file(renpy_init_py):
        inject_code = 'import renpy.translation.projz_inject'
        target_code = 'import renpy.translation.generation'
        try:
            new_lines = []
            with open(renpy_init_py, 'r', encoding='utf-8', newline='\n') as f:
                all_lines = f.readlines()
            for i, line in enumerate(all_lines):
                code = line.strip()
                # print(code)
                if code:
                    if code == inject_code:
                        new_lines = all_lines
                        break
                    if code == target_code:
                        new_lines = all_lines[:i] + [line.replace(target_code, inject_code)] + all_lines[i:]
                        break
            assert new_lines, f'Coundn\'t find the code({inject_code}) to inject in {renpy_init_py}'
            with open(renpy_init_py, 'w', encoding='utf-8', newline='\n') as f:
                f.writelines(new_lines)
            shutil.copy('projz_inject.py', injection_py)
        except Exception as e:
            # roll back
            try:
                if all_lines:
                    with open(renpy_init_py, 'w', encoding='utf-8', newline='\n') as f:
                        f.writelines(all_lines)
            except:
                pass
            try:
                os.remove(injection_py)
            except:
                pass
            raise e

def do_launch_test(project):
    str_id = uuid.uuid1().hex
    json_file = os.path.join(os.path.abspath('.'), 'tmp.json')
    code = project.launch('projz_inject_command', args=[json_file,
                                           f'--uuid {str_id}',  '--test-only'], wait=True)
    if code == 0:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if data['ok']:
                    return True
        # except:
        #     pass
        finally:
            try:
                os.remove(json_file)
                # pass
            except:
                pass
    return False

class Project:

    def __init__(self, project_path, executable_path, project_name):
        self.project_path = project_path
        self.executable_path = executable_path
        self.project_name = project_name


    def launch(self, cmd, args, wait=False):
        # Put together the basic command line.
        cmd_line = [self.executable_path, os.path.join(self.project_path, f'{self.project_name}.py'),
               self.project_path, cmd, ' '.join(args)]
        # print(' '.join(cmd_line))
        # return None
        p = subprocess.Popen(' '.join(cmd_line))
        if wait:
            return_code = p.wait()
            print(return_code)
            return return_code
        return None


    @classmethod
    def from_dir(cls, project_path):
        abs_path = os.path.abspath(project_path)

        # check the dir structure
        check_renpy_dir(abs_path)

        # find the project name
        project_name = find_project_name(abs_path)

        # Get the executable python
        executable_path = find_exe(abs_path)

        # check and inject
        do_injection(abs_path)

        # print(abs_path)
        # print(executable_path)
        # print(project_name)
        return cls(abs_path, executable_path, project_name)


if __name__ == '__main__':
    p = Project.from_dir(r'D:\BaiduNetdiskDownload\New31\ScarletTrainer-0.2-pc')
    print(uuid.uuid1().hex)
    print(do_launch_test(p))
    # p.launch('projz_inject_command', args=[r'D:\BaiduNetdiskDownload\New31\ScarletTrainer-0.2-pc\translation.json',
    #                                        f'--uuid {uuid.uuid1().hex}', '--language chinese', '--all-strings', '--count'], wait=True)
