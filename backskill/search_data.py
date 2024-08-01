# _*_ coding: utf-8 _*_
# @File:    search_data
# @Time:    2024/5/13 11:29
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


def search_in_database(search_keywords, search_model, columns_to_select, column_mapping):
    # 连接数据库
    conn = connect_to_database()
    # 创建游标对象
    cursor = conn.cursor()

    try:
        # 构建查询条件
        conditions = []
        query_parameters = []

        for keyword in search_keywords:
            conditions.append("模型名称（中文） LIKE %s")
            query_parameters.append('%' + keyword + '%')

        # 如果有模型名称限制，则添加到条件中
        if search_model:
            conditions.append("标签 = %s")
            query_parameters.append(search_model)

        # 构建完整的查询语句
        query = f"SELECT {', '.join(columns_to_select)} FROM modelist WHERE {' AND '.join(conditions)}"

        # 执行查询语句
        cursor.execute(query, query_parameters)

        # 获取查询结果
        result = {}
        for row in cursor.fetchall():
            key = row[0]  # 第一列作为外部字典的键
            inner_dict = {}
            for i, column in enumerate(columns_to_select[1:], start=1):
                # 将列名映射为英文
                english_column_name = column_mapping.get(column, column)
                inner_dict[english_column_name] = row[i]  # 内部字典的键是映射后的英文列名，值是列值
            result[int(key) - 1] = inner_dict

        return result

    except mysql.connector.Error as err:
        print("Error:", err)

    finally:
        # 关闭游标和连接
        cursor.close()
        conn.close()

key_mapping = {
    '模型名称（中文）': 'chineseName',
    '模型名称（英文）': 'englishName',
    '运行语言': 'language',
    '标签': 'label',
    '所属产线': 'productionLine',
    '所属工序': 'process',
    '参数描述': 'parameterDescription',
    '测试代码': 'predictCode',
    '测试结果样例': 'resultSample'
}

search_keywords = '计算,应力'
search_keywords = search_keywords.split(",")
result = search_in_database(search_keywords, '',
                            ['序号', '模型名称（中文）', '模型名称（英文）', '运行语言', '标签', '所属产线'], key_mapping)
# def count_rows_by_search(search_keyword):
#
#     conn = connect_to_database()
#     cursor = conn.cursor()
#     query = f"SELECT COUNT(*) FROM modelist WHERE 模型名称（中文） LIKE %s"
#     cursor.execute(query, ('%' + search_keyword + '%',))
#
#     count = cursor.fetchone()[0]
#     cursor.close()
#     conn.close()
#     return count
# search_keyword = input("Enter search keyword: ")
# current_model_num = count_rows_by_search(search_keyword)
# print(current_model_num)
# def count_rows_by_search(search_keywords, search_model):
#     conn = connect_to_database()
#     cursor = conn.cursor()
#
#     try:
#         # 构建查询条件
#         conditions = []
#         query_parameters = []
#
#         for keyword in search_keywords:
#             conditions.append("模型名称（中文） LIKE %s")
#             query_parameters.append('%' + keyword + '%')
#
#         # 如果有模型名称限制，则添加到条件中
#         if search_model:
#             conditions.append("标签 = %s")
#             query_parameters.append(search_model)
#
#         # 构建完整的查询语句
#         query = f"SELECT COUNT(*) FROM modelist WHERE {' AND '.join(conditions)}"
#
#         # 执行查询语句
#         cursor.execute(query, query_parameters)
#
#         # 获取查询结果
#         count = cursor.fetchone()[0]
#
#         return count
#
#     except mysql.connector.Error as err:
#         print("Error:", err)
#
#     finally:
#         # 关闭游标和连接
#         cursor.close()
#         conn.close()
#
#
# # 调用函数并输入要搜索的内容
# search_keywords = input("Enter search keywords separated by commas: ").split(',')
# count = count_rows_by_search(search_keywords, '')
# print(count)
