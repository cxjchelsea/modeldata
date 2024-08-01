# _*_ coding: utf-8 _*_
# @File:    select_columns
# @Time:    2024/4/16 15:16
# @Author:  chenxuejiao
# @Contact: 15801102378@163.com
# @Version: V 0.1
import mysql.connector
def connect_to_database():
    """连接到MySQL数据库"""
    conn = mysql.connector.connect(
        host='localhost',
        database='test',
        user='root',
        password='123456',
        auth_plugin='mysql_native_password'
    )
    return conn

import mysql.connector
# def get_column_name_by_index(table_name, column_index):
#     try:
#         # 连接到 MySQL 数据库
#         connection = connect_to_database()
#
#         if connection.is_connected():
#             cursor = connection.cursor()
#
#             # 执行 SQL 查询以获取表的列名和类型
#             cursor.execute("SHOW COLUMNS FROM {}".format(table_name))
#
#             # 获取所有列名和类型的元组列表
#             columns_info = cursor.fetchall()
#
#             # 检查索引是否有效
#             if 0 <= column_index < len(columns_info):
#                 column_name = columns_info[column_index][0]
#
#                 # 关闭游标和连接
#                 cursor.close()
#                 connection.close()
#
#                 return column_name
#             else:
#                 print("无效的列索引")
#                 return None
#         else:
#             print("无法连接到数据库")
#             return None
#     except Exception as e:
#         print("发生错误:", e)
#         return None
## 筛选选项下拉菜单
# conn = connect_to_database()
# cursor = conn.cursor()
# query = "SELECT * FROM information_roll_line"  # 获取所有列的数据
# cursor.execute(query)
# data = cursor.fetchall()
# selected_column_index = 1
# selected_column_data = [row[selected_column_index] for row in data]
# selected_line_options = list(set(selected_column_data))
# cursor.close()
# conn.close()
# print(selected_line_options)

## 筛选某一项
# selected_line = '敬业1780mm热连轧'
# selected_line_index = 1  # 假设您想按照第三列（索引为2）的值来筛选
# column_name = get_column_name_by_index('information_roll_line', selected_line_index)
# conn = connect_to_database()
# cursor = conn.cursor()
# query = f"SELECT * FROM information_roll_line WHERE {column_name} = %s"  # 使用%s作为占位符
# cursor.execute(query, (selected_line,))
# data = cursor.fetchall()
# cursor.close()
# conn.close()


