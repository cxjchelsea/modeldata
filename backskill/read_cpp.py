# _*_ coding: utf-8 _*_
# @File:    read_cpp
# @Time:    2024/5/27 13:55
# @Author:  chenxuejiao
# @Contact: 15801102378@163.com
# @Version: V 0.1
import os
import chardet
import time
from pywinauto import Application
import pywinauto.keyboard as keyboard
import os

def create_dll_project(project_name, h_code, cpp_code):
    visual_studio_path = r"C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\devenv.exe"
    project_dir = os.path.join("E:/visual studio", project_name, project_name)
    app = Application(backend='uia').start(visual_studio_path)
    time.sleep(5)
    keyboard.send_keys("%N")
    time.sleep(2)
    keyboard.send_keys("{ENTER}")
    time.sleep(2)
    keyboard.send_keys(project_name)
    keyboard.send_keys("{ENTER}")
    time.sleep(5)

    keyboard.send_keys("^+A")
    time.sleep(2)
    keyboard.send_keys("{TAB}{TAB}{DOWN}{DOWN}")
    time.sleep(2)
    keyboard.send_keys("{TAB}")
    time.sleep(2)
    keyboard.send_keys(f"{project_name}.h")
    time.sleep(2)
    keyboard.send_keys("{ENTER}")
    time.sleep(5)

    keyboard.send_keys("^+A")
    time.sleep(2)
    keyboard.send_keys("{TAB}{TAB}{DOWN}{UP}")
    time.sleep(2)
    keyboard.send_keys("{TAB}")
    time.sleep(2)
    keyboard.send_keys(f"{project_name}.cpp")
    time.sleep(2)
    keyboard.send_keys("{ENTER}")
    time.sleep(5)

    header_path = os.path.join(project_dir, f"{project_name}.h")
    with open(header_path, "w") as header_file:
        header_file.write(h_code)

    header_path = os.path.join(project_dir, f"{project_name}.cpp")
    with open(header_path, "w") as header_file:
        header_file.write(cpp_code)

    time.sleep(5)
    keyboard.send_keys("^+B")
    time.sleep(10)
    error_popup = app.window(title="Error List")
    if error_popup.exists():
        print(f"项目 '{project_name}' 编译失败！")
    app.kill()
    time.sleep(2)
def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        return result['encoding']

def read_cpp_files(folder_path):
    cpp_files_data = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".cpp"):
            file_path = os.path.join(folder_path, filename)
            cpp_files_data[filename] = read_cpp_file(file_path)
    return cpp_files_data
def read_cpp_file(file_path):
    try:
        encoding = detect_encoding(file_path)
        with open(file_path, 'r', encoding=encoding) as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return f"文件 {file_path} 未找到。"
    except UnicodeDecodeError:
        return f"无法使用检测到的编码 {encoding} 读取文件 {file_path}。"
    except IOError:
        return f"读取文件 {file_path} 时出错。"
def extract_substring_between_chars(input_string, start_char, end_char=None):
    start_index = input_string.find(start_char)
    if start_index != -1:
        if end_char:
            end_index = input_string.find(end_char, start_index + 1)
            if end_index != -1:
                return input_string[start_index:end_index + 1]
        else:
            return input_string[start_index:]
    return None
def string_cpp_content(cpp_code, filename):
    index_open_brace = cpp_code.find('extern "C"') + len('extern "C"')
    index_last_close_brace = cpp_code.rfind("}")
    filename = os.path.splitext(filename)[0]
    cpp_code = '#include "pch.h"\n' + f'#include "{filename}.h"\n' + '#include <cmath>\n' + cpp_code[:index_open_brace] + ' __declspec(dllexport)' + cpp_code[index_open_brace + 1:index_last_close_brace]
    return cpp_code
h_content = """
#ifdef SIMPLEADDER_EXPORTS
#define SIMPLEADDER_API __declspec(dllexport)
#else
#define SIMPLEADDER_API __declspec(dllimport)
#endif
extern "C" SIMPLEADDER_API
"""
folder_path = "cpp"
cpp_files_data = read_cpp_files(folder_path)
for filename, code in cpp_files_data.items():
    start_h = "{"
    end_h = ")"
    h_code = extract_substring_between_chars(code, start_h, end_h)
    h_code = h_content + h_code[1:] + ";"
    start_cpp = "extern"
    cpp_code = extract_substring_between_chars(code, start_cpp)
    cpp_code = string_cpp_content(cpp_code, filename)
    project_name = os.path.splitext(filename)[0]
    create_dll_project(project_name, h_code, cpp_code)


