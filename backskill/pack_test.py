# _*_ coding: utf-8 _*_
# @File:    pack_test
# @Time:    2024/5/27 10:00
# @Author:  chenxuejiao
# @Contact: 15801102378@163.com
# @Version: V 0.1

import time
from pywinauto import Application
import pywinauto.keyboard as keyboard
import os

def create_dll_project(project_name):
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
    keyboard.send_keys("SimpleAdder.h")
    time.sleep(2)
    keyboard.send_keys("{ENTER}")
    time.sleep(5)

    keyboard.send_keys("^+A")
    time.sleep(2)
    keyboard.send_keys("{TAB}{TAB}{DOWN}{UP}")
    time.sleep(2)
    keyboard.send_keys("{TAB}")
    time.sleep(2)
    keyboard.send_keys("SimpleAdder.cpp")
    time.sleep(2)
    keyboard.send_keys("{ENTER}")
    time.sleep(5)

    h_content = """
#ifdef SIMPLEADDER_EXPORTS
#define SIMPLEADDER_API __declspec(dllexport)
#else
#define SIMPLEADDER_API __declspec(dllimport)
#endif
extern "C" SIMPLEADDER_API int Add(int a, int b);
"""
    header_path = os.path.join(project_dir, "SimpleAdder.h")
    with open(header_path, "w") as header_file:
        header_file.write(h_content)

    cpp_content = """
#include "pch.h"
#include "SimpleAdder.h"
int Add(int a, int b) {
    return a + b;
}
"""
    header_path = os.path.join(project_dir, "SimpleAdder.cpp")
    with open(header_path, "w") as header_file:
        header_file.write(cpp_content)

    time.sleep(5)
    keyboard.send_keys("^+B")
    time.sleep(5)

    app.kill()
project_name = "SimpleAdder"
create_dll_project(project_name)

