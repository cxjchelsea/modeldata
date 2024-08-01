# _*_ coding: utf-8 _*_
# @File:    example.py
# @Time:    2024/5/15 14:01
# @Author:  chenxuejiao
# @Contact: 15801102378@163.com
# @Version: V 0.1

import ctypes

dll_path = "./to test/Gap_Oil_Film_Factor.dll"
model = ctypes.CDLL(dll_path)
model.Gap_Oil_Film_Factor.argtypes = [ctypes.c_float, ctypes.c_int, ctypes.c_float, ctypes.c_float, ctypes.c_float]#, ctypes.c_float, ctypes.c_float, ctypes.c_float
model.Gap_Oil_Film_Factor.restype = ctypes.c_float
h0=800
h1=7
R=10
t=200
v0=10
# a=1.5
# b=1
# c=0.2

result = model.Gap_Oil_Film_Factor(h0,h1,R,t,v0)#,a,b,c
print(result)

# import ctypes
# import mysql.connector
# import json
# def connect_to_database():
#     """连接到MySQL数据库"""
#     conn = mysql.connector.connect(
#         host='localhost',
#         database='test',
#         user='root',
#         password='19990118',
#         auth_plugin='mysql_native_password'
#     )
#     return conn
# my_dll = ctypes.cdll.LoadLibrary("./totest/Bending_Factor_Gap.dll")
# function_name = "Bending_Factor_Gap"
# param_types = ['float', 'float', 'float']
# conn = connect_to_database()
# cursor = conn.cursor()
# query = f"SELECT 测试代码 FROM modelist WHERE 模型名称（英文） = %s"
# cursor.execute(query, (function_name,))
# result = cursor.fetchall()[0]
# cursor.close()
# conn.close()
# data = json.loads(result[0])["req_data"]
# params = list(data.values())
# my_function = getattr(my_dll, function_name)
# my_function.argtypes = [eval('ctypes.c_' + t) for t in param_types]
# my_function.restype = eval('ctypes.c_' + param_types[1])
# result = my_function(*params)
# print(f"Temperature rise: {result}")

# import os
# import shutil
# def find_files(root_dir, depth=1, target_ext='.cpp'):
# # def find_files(root_dir, depth=3, target_ext='.dll'):
#
#     found_files = []
#
#     # 递归函数，遍历文件夹
#     def recurse_directory(directory, current_depth):
#         if current_depth > depth:
#             return
#         for item in os.listdir(directory):
#             item_path = os.path.join(directory, item)
#             if os.path.isdir(item_path):
#                 recurse_directory(item_path, current_depth + 1)
#             elif os.path.isfile(item_path) and item_path.endswith(target_ext):
#                 found_files.append(item_path)
#
#     recurse_directory(root_dir, 0)
#     return found_files
#
# root_directory = './已生成cpp/文件夹'
# target_directory = './cpp'
# # root_directory = 'E:/visual studio'
# # target_directory = './totest'
# found_files = find_files(root_directory)
# for file_path in found_files:
#     file_name = os.path.basename(file_path)
#     shutil.copy(file_path, os.path.join(target_directory, file_name))


