# _*_ coding: utf-8 _*_
# @File:    query_data_in_range
# @Time:    2024/4/18 10:02
# @Author:  chenxuejiao
# @Contact: 15801102378@163.com
# @Version: V 0.1
import mysql.connector
import math
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
def query_range(table, selected_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    query_max_id = f"SELECT MAX(ID) FROM {table}"
    cursor.execute(query_max_id)
    max_id = int(cursor.fetchone()[0])  # 将最大ID转换为整数

    if int(selected_id) > max_id:  # 将selected_id转换为整数再进行比较
        query = f"SELECT * FROM {table} WHERE ID = %s"
        cursor.execute(query, (max_id,))
    else:
        query = f"SELECT * FROM {table} WHERE ID = %s"
        cursor.execute(query, (selected_id,))

    data = cursor.fetchall()
    cursor.close()
    conn.close()

    if int(selected_id) > max_id:  # 同样需要将selected_id转换为整数
        min_val = data[0][2]
        max_val = float('inf')
    else:
        min_val = data[0][1]
        max_val = data[0][2]

    return min_val, max_val

def query_data_in_range(table, column, min_value, max_value, page, page_size):
    # 连接到MySQL数据库
    conn = connect_to_database()
    # 创建游标对象
    cursor = conn.cursor()
    try:
        offset = (page - 1) * page_size
        if max_value == float('inf'):
            query = f"SELECT * FROM {table} WHERE {column} >= %s LIMIT %s OFFSET %s"
            cursor.execute(query, (min_value, page_size, offset))
            print(query)
        else:
            query = f"SELECT * FROM {table} WHERE {column} >= %s AND {column} < %s LIMIT %s OFFSET %s"
            cursor.execute(query, (min_value, max_value, page_size, offset))
        results = cursor.fetchall()

        if max_value == float('inf'):
            count_query = f"SELECT COUNT(*) FROM {table} WHERE {column} >= %s"
            cursor.execute(count_query, (min_value,))
        else:
            count_query = f"SELECT COUNT(*) FROM {table} WHERE {column} >= %s AND {column} < %s"
            cursor.execute(count_query, (min_value, max_value))
        total_rows = cursor.fetchone()[0]

        # 计算总页数
        total_pages = math.ceil(total_rows / page_size)

        return {'Data': results, 'totalPages': total_pages}

    except mysql.connector.Error as err:
        print("MySQL错误:", err)

    finally:
        # 关闭游标和连接
        cursor.close()
        conn.close()


selected_width = '17'
selected_pline = 'jt2250'
tgt_wid = 'T_Wid'
min_width, max_width = query_range('width', selected_width)
result = query_data_in_range('jt2250', 'T_Wid', min_width, max_width, 1, 10)