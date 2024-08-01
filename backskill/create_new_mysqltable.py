# _*_ coding: utf-8 _*_
# @File:    create_new_mysqltable
# @Time:    2024/3/25 10:03
# @Author:  chenxuejiao
# @Contact: 15801102378@163.com
# @Version: V 0.1

import pandas as pd
import mysql.connector
from mysql.connector import Error
import re

def fix_column_names(columns):
    fixed_columns = []
    for col in columns:
        # 将整数转换为字符串
        if isinstance(col, int):
            col = str(col)
        # 删除特殊字符
        col = re.sub(r'[^\w\s]', '', col)
        if col[0].isdigit():
            fixed_columns.append("col_" + col)
        else:
            fixed_columns.append(col)
    return fixed_columns

def get_mysql_data_type(column):
    if pd.api.types.is_integer_dtype(column):
        return "INT"
    elif pd.api.types.is_float_dtype(column):
        return "FLOAT"
    else:
        return "VARCHAR(50)"


excel_file = 'E:\\1Study&Work\modeldata\数据存档\模型库\modelist.xlsx'
df = pd.read_excel(excel_file)
table_name = 'modelist'
connection = None
cursor = None

try:
    connection = mysql.connector.connect(
        host='localhost',
        database='test',
        user='root',
        password='123456',
        auth_plugin='mysql_native_password'
    )
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("已连接到 MySQL 服务器版本 ", db_Info)
        cursor = connection.cursor()
except Error as e:
    print("连接到 MySQL 时出错", e)

if cursor:
    # 获取 Excel 列名和数据类型
    columns = list(df.columns)
    print(columns)  # 输出列名以便检查
    data_types = [get_mysql_data_type(df[col]) for col in df.columns]

    # 修复列名
    fixed_columns = fix_column_names(columns)

    # 生成创建表格的 SQL 语句
    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ("
    create_table_query += ", ".join([f"`{col}` {data_types[i]}" for i, col in enumerate(fixed_columns)])
    create_table_query += ")"

    try:
        cursor.execute(create_table_query)
        print("表格创建成功")
    except Error as e:
        print("创建表格时出错", e)


if connection and connection.is_connected():
    cursor.close()
    connection.close()
    print("MySQL 连接已关闭")


# def fix_column_names(columns):
#     fixed_columns = []
#     for col in columns:
#         # 将整数转换为字符串
#         if isinstance(col, int):
#             col = str(col)
#         # 删除特殊字符
#         col = re.sub(r'[^\w\s]', '', col)
#         if col[0].isdigit():
#             fixed_columns.append("col_" + col)
#         else:
#             fixed_columns.append(col)
#     return fixed_columns
#
# def get_mysql_data_type(column):
#     if pd.api.types.is_integer_dtype(column):
#         return "INT"
#     elif pd.api.types.is_float_dtype(column):
#         return "FLOAT"
#     else:
#         return "VARCHAR(50)"
#
#
# csv_file = "2160/H11.202205.csv"
# df = pd.read_csv(csv_file)
#
# connection = None
# cursor = None
#
# try:
#     connection = mysql.connector.connect(
#         host='localhost',
#         database='test',
#         user='root',
#         password='123456',
#         auth_plugin='mysql_native_password'
#     )
#     if connection.is_connected():
#         db_Info = connection.get_server_info()
#         print("已连接到 MySQL 服务器版本 ", db_Info)
#         cursor = connection.cursor()
# except Error as e:
#     print("连接到 MySQL 时出错", e)
#
# if cursor:
#     # 获取 CSV 列名和数据类型
#     columns = list(df.columns)
#     print(columns)  # 输出列名以便检查
#     data_types = [get_mysql_data_type(df[col]) for col in df.columns]
#
#     # 修复列名
#     fixed_columns = fix_column_names(columns)
#
#     # 生成创建表格的 SQL 语句
#     create_table_query = "CREATE TABLE IF NOT EXISTS qiangang2160 ("
#     create_table_query += ", ".join([f"`{col}` {data_types[i]}" for i, col in enumerate(fixed_columns)])
#     create_table_query += ")"
#
#     try:
#         cursor.execute(create_table_query)
#         print("表格创建成功")
#     except Error as e:
#         print("创建表格时出错", e)
#
#
# if connection and connection.is_connected():
#     cursor.close()
#     connection.close()
#     print("MySQL 连接已关闭")
