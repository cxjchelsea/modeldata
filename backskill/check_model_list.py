# _*_ coding: utf-8 _*_
# @File:    check_model_list
# @Time:    2024/4/17 15:33
# @Author:  chenxuejiao
# @Contact: 15801102378@163.com
# @Version: V 0.1

import mysql.connector

table_name = "modelist"
column1 = "标签"
value1 = "负荷分配"
column2 = "所属产线"
value2 = "中厚板"
def count_rows_with_values(table_name, column1, value1, column2, value2):

    conn = mysql.connector.connect(
        host='localhost',
        database='model_data_base',
        user='root',
        password='123456',
        auth_plugin='mysql_native_password'
    )
    cursor = conn.cursor()
    query = f"SELECT COUNT(*) FROM {table_name} WHERE {column1} = %s AND {column2} = %s"
    cursor.execute(query, (value1, value2))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count
count = count_rows_with_values(table_name, column1, value1, column2, value2)
print(count)