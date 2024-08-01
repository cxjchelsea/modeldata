# _*_ coding: utf-8 _*_
# @File:    read_columns_data
# @Time:    2024/4/16 8:52
# @Author:  chenxuejiao
# @Contact: 15801102378@163.com
# @Version: V 0.1

import pandas as pd
import mysql.connector
def read_excel_column(file_path, sheet_name, column_name):
    try:
        # 读取 Excel 文件
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        # 提取指定列的数据
        column_data = df[column_name].tolist()
        return column_data
    except Exception as e:
        print("Error:", e)

# 示例用法
file_path = 'information_roll_line_name_with_id.xls'  # Excel 文件路径
sheet_name = 'sheet1'        # 工作表名称
column_name = 'chinese_name'      # 要读取的列名称

data = read_excel_column(file_path, sheet_name, column_name)

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

def modify_table_headers(table, new_column_names):
    try:
        # 连接到 MySQL 数据库
        conn = connect_to_database()

        # 创建游标
        cursor = conn.cursor()

        # 获取当前表的列名
        cursor.execute(f"SHOW COLUMNS FROM {table}")
        current_column_names = [column[0] for column in cursor.fetchall()]

        # 检查输入数组和当前列名的长度是否一致
        if len(new_column_names) != len(current_column_names):
            print("输入数组和当前列名的长度不一致。")
            return

        # 使用 zip() 函数将新旧列名配对，然后逐一修改列名
        for old_column_name, new_column_name in zip(current_column_names, new_column_names):
            modify_query = f"ALTER TABLE {table} CHANGE COLUMN {old_column_name} {new_column_name} VARCHAR(255)"
            cursor.execute(modify_query)

        # 提交事务
        conn.commit()

        print("表头修改成功。")

    except mysql.connector.Error as err:
        print("Error:", err)

    finally:
        # 关闭游标和连接
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

# 示例用法
table = 'information_roll_line'
new_column_names = data
modify_table_headers(table, new_column_names)
