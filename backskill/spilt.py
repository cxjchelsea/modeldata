# _*_ coding: utf-8 _*_
# @File:    spilt
# @Time:    2024/4/14 23:32
# @Author:  chenxuejiao
# @Contact: 15801102378@163.com
# @Version: V 0.1

# def split_string(input_string):
#     # 使用 split() 方法按照 '-' 进行分割
#     parts = input_string.split('-')
#     return parts
#
# # 示例用法
# current_page = "力能参数-热连轧"
# label = split_string(current_page)[0]
# pline = split_string(current_page)[1]
# print(label)
# print(pline)
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
def extract_data(column1, value1, column2, value2, columns_to_select, column_mapping):
    try:
        # 连接到MySQL数据库
        conn = connect_to_database()

        cursor = conn.cursor()

        # 执行查询
        query = f"SELECT {', '.join(columns_to_select)} FROM modelist WHERE {column1} = %s AND {column2} = %s"

        cursor.execute(query, (value1, value2))
        # 处理结果并生成嵌套的键值对
        result = {}
        for row in cursor.fetchall():
            key = row[0]  # 第一列作为外部字典的键
            print(key)
            inner_dict = {}
            for i, column in enumerate(columns_to_select[1:], start=1):
                # 将列名映射为英文
                english_column_name = column_mapping.get(column, column)
                inner_dict[english_column_name] = row[i]  # 内部字典的键是映射后的英文列名，值是列值
            result[int(key)-1] = inner_dict

        return result
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        raise
    finally:
        # 关闭连接
        if 'conn' in locals():
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
result = extract_data('标签', '负荷分配', '所属产线', '热连轧', ['序号','模型名称（中文）', '模型名称（英文）', '运行语言', '标签'], key_mapping)
print(result)