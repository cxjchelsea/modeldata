# _*_ coding: utf-8 _*_
# @File:    read_mysql_as_dicts
# @Time:    2024/4/9 11:09
# @Author:  chenxuejiao
# @Contact: 15801102378@163.com
# @Version: V 0.1
import mysql.connector

def connect_to_database():
    """连接到MySQL数据库"""
    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='model_data_base',
            user='root',
            password='123456',
            auth_plugin='mysql_native_password'
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        raise

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

# 示例用法
column1 = '标签'
value1 = '力能参数'
column2 = '所属产线'
value2 = '冷轧'
columns_to_select = ['序号','模型名称（中文）', '模型名称（英文）', '运行语言', '标签']
column_mapping = {
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
data = extract_data(column1, value1, column2, value2, columns_to_select, column_mapping)
print(data)