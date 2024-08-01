# _*_ coding: utf-8 _*_
# @File:    read_mysql_line
# @Time:    2024/4/15 14:39
# @Author:  chenxuejiao
# @Contact: 15801102378@163.com
# @Version: V 0.1

import mysql.connector
def connect_to_database():
    """连接到MySQL数据库"""
    conn = mysql.connector.connect(
        host='localhost',
        database='model_data_base',
        user='root',
        password='123456',
        auth_plugin='mysql_native_password'
    )
    return conn
def get_row_count(table_name):
    try:
        # 连接到 MySQL 数据库
        connection = connect_to_database()

        if connection.is_connected():
            # 创建游标对象
            cursor = connection.cursor()

            # 执行查询
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")

            # 获取结果
            row_count = cursor.fetchone()[0]

            # 关闭游标和连接
            cursor.close()
            connection.close()

            return row_count
        else:
            print("连接失败！")
            return None

    except mysql.connector.Error as e:
        print(f"发生错误：{e}")
        return None

# 调用函数并打印结果
table_name = ("shagang")
count = get_row_count(table_name)
if count is not None:
    print(f"表 {table_name} 的行数为：{count}")
