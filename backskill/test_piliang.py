# _*_ coding: utf-8 _*_
# @File:    test_piliang
# @Time:    2024/5/30 16:09
# @Author:  chenxuejiao
# @Contact: 15801102378@163.com
# @Version: V 0.1
import os
import re
import ctypes
import mysql.connector
import json
def extract_function_signatures(directory):
    cpp_files = [f for f in os.listdir(directory) if f.endswith('.cpp')]
    functions_info = {}

    # Regular expression to match function declarations inside extern "C"
    extern_c_pattern = re.compile(r'extern\s+"C"\s*{[^}]*}')
    func_pattern = re.compile(r'\b([a-zA-Z_]\w*)\s+([a-zA-Z_]\w*)\s*\(([^)]*)\)')

    for cpp_file in cpp_files:
        file_name_without_ext = os.path.splitext(cpp_file)[0]
        functions_info[file_name_without_ext] = []
        with open(os.path.join(directory, cpp_file), 'r', encoding='latin-1') as file:
            content = file.read()
            extern_c_blocks = extern_c_pattern.findall(content)
            for block in extern_c_blocks:
                matches = func_pattern.findall(block)
                for match in matches:
                    return_type = match[0]
                    func_name = match[1]
                    params = match[2].split(',') if match[2] else []
                    param_types = [param.strip().split()[0] for param in params if param.strip()]
                    functions_info[file_name_without_ext].append((func_name, param_types))

    return functions_info
def connect_to_database():
    """连接到MySQL数据库"""
    conn = mysql.connector.connect(
        host='localhost',
        database='test',
        user='root',
        password='123456',
        auth_plugin='mysql_native_password',
        charset = 'utf8'
    )
    return conn

# 使用示例
directory = 'C:/Users/1/Desktop/临时文件夹/新建文件夹/新建文件夹'
functions_info = extract_function_signatures(directory)
for filename, funcs in functions_info.items():
    my_dll = ctypes.cdll.LoadLibrary(f"./totest/{filename}.dll")
    for func_name, param_types in funcs:
        conn = connect_to_database()
        cursor = conn.cursor()
        query = f"SELECT 测试代码 FROM modelist WHERE 模型名称（英文） = %s"
        cursor.execute(query, (func_name,))
        result = cursor.fetchall()[0]
        cursor.close()
        conn.close()
        data = json.loads(result[0])["req_data"]
        params = list(data.values())
        my_function = getattr(my_dll, func_name)
        my_function.argtypes = [eval('ctypes.c_' + t) for t in param_types]
        my_function.restype = eval('ctypes.c_' + param_types[1])
        result = my_function(*params)
        print(result)