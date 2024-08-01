# _*_ coding: utf-8 _*_
# @File:    read_header
# @Time:    2024/4/15 17:21
# @Author:  chenxuejiao
# @Contact: 15801102378@163.com
# @Version: V 0.1

import mysql.connector

def connect_to_database():
    """连接到 MySQL 数据库"""
    conn = mysql.connector.connect(
        host='localhost',
        database='test',
        user='root',
        password='123456',
        auth_plugin='mysql_native_password'
    )
    return conn

def read_table_headers(table):
    try:
        # 连接到 MySQL 数据库
        conn = connect_to_database()

        # 创建游标
        cursor = conn.cursor()

        # 执行 SHOW COLUMNS 查询获取表头信息
        cursor.execute(f"SHOW COLUMNS FROM {table}")

        # 提取列名
        column_names = [column[0] for column in cursor.fetchall()]

        return column_names

    except mysql.connector.Error as err:
        print("Error:", err)

    finally:
        # 关闭游标和连接
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

# 示例用法
header = read_table_headers("information_roll_line")
print(header)