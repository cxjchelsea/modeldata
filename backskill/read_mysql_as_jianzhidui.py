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
def read_table_to_dict(table, key_column, value_column):
    try:
        # 连接到 MySQL 数据库
        conn = connect_to_database()

        # 创建游标
        cursor = conn.cursor()

        # 执行 SQL 查询获取表中的数据
        query = f"SELECT {key_column}, {value_column} FROM {table}"
        cursor.execute(query)

        # 构建键值对字典
        result = {row[0]: row[1] for row in cursor.fetchall()}

        return result

    except mysql.connector.Error as err:
        print("Error:", err)

    finally:
        # 关闭游标和连接
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

# 示例用法
result = read_table_to_dict("product_roll_line_name", "roll_line", "line_number")
print(result)
total_sum = sum(result.values())
print("总和:", total_sum)
