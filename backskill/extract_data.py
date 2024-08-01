# _*_ coding: utf-8 _*_
# @File:    extract_data
# @Time:    2024/5/13 9:56
# @Author:  chenxuejiao
# @Contact: 15801102378@163.com
# @Version: V 0.
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
        if (value1 == '*' and value2 == '*'):
            # 执行查询
            query = f"SELECT {', '.join(columns_to_select)} FROM modelist"
            print("查询语句:", query)  # 打印查询语句
            cursor.execute(query)
        elif (value1 != '*' and value2 == '*'):
            # 执行查询
            query = f"SELECT {', '.join(columns_to_select)} FROM modelist WHERE {column1} = '{value1}'"
            print("查询语句:", query)  # 打印查询语句
            cursor.execute(query)
        else:
            # 执行查询
            query = f"SELECT {', '.join(columns_to_select)} FROM modelist WHERE {column1} = '{value1}' AND {column2} = '{value2}'"
            print("查询语句:", query)  # 打印查询语句
            cursor.execute(query)


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
result = extract_data('标签', '力能参数', '所属产线', '热连轧',
                      ['序号', '模型名称（中文）', '模型名称（英文）', '运行语言', '标签', '所属产线'], key_mapping)


print(result)
