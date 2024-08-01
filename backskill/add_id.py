# _*_ coding: utf-8 _*_
# @File:    fenge_excel
# @Time:    2024/3/25 9:54
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
def delete_column(table_name):
    conn = connect_to_database()
    cursor = conn.cursor()
    alter_query = f"ALTER TABLE {table_name} DROP COLUMN 序号"
    cursor.execute(alter_query)
    conn.commit()
    cursor.close()
    conn.close()

def add_serial_number_column(table_name):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute(f"SHOW COLUMNS FROM {table_name} LIKE '序号'")
    result = cursor.fetchone()
    if result:
        cursor.execute(f"ALTER TABLE {table_name} DROP COLUMN ID")
    cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN ID INT AUTO_INCREMENT PRIMARY KEY FIRST")
    cursor.execute(f"SET @row_number = 0")
    cursor.execute(f"UPDATE {table_name} SET ID = (@row_number:=@row_number+1)")
    conn.commit()
    cursor.close()
    conn.close()
    print("序号列添加成功，并已生成序号信息。")



def update_ID(table_name):
    # delete_column(table_name)
    add_serial_number_column(table_name)

update_ID('shangang')