# _*_ coding: utf-8 _*_
# @File:    modelku
# @Time:    2024/4/15 15:06
# @Author:  chenxuejiao
# @Contact: 15801102378@163.com
# @Version: V 0.1

import json
import requests
from flask import Flask, jsonify, request
import pandas as pd
import mysql.connector
import math
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

users = [
    {'username': 'admin', 'password': 'admin123', 'role': 'admin'},
    {'username': 'user', 'password': 'user123', 'role': 'user'},
]
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
def get_table_columns(table):
    try:
        # 连接到 MySQL 数据库
        conn = connect_to_database()

        if conn.is_connected():
            cursor = conn.cursor()

            # 执行 DESC 查询获取表结构信息
            query = f"DESCRIBE {table}"
            cursor.execute(query)

            # 读取查询结果
            columns = [column[0] for column in cursor.fetchall()]

            # 打印表头列名数组
            return columns

    except mysql.connector.Error as error:
        print("Error reading table columns from MySQL:", error)

    finally:
        cursor.close()
        conn.close()
def get_column_data(column, table):
    try:
        # 连接到 MySQL 数据库
        connection = connect_to_database()

        if connection.is_connected():
            cursor = connection.cursor()

            # 执行查询以获取特定列的数据
            query = f"SELECT {column} FROM {table}"
            cursor.execute(query)

            # 读取查询结果并将其存储在数组中
            column_data = [row[0] for row in cursor.fetchall()]

            return column_data

    except mysql.connector.Error as error:
        print("Error reading column data from MySQL:", error)
        return []

    finally:
        cursor.close()
        connection.close()
def get_row_count(table_name):
    try:
        # 连接到 MySQL 数据库
        connection = connect_to_database()

        if connection.is_connected():
            # 创建游标对象
            cursor = connection.cursor()

            # 执行查询
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")

            # 获取结果
            row_count = cursor.fetchone()[0]

            # 关闭游标和连接
            cursor.close()
            connection.close()

            return row_count
        else:
            print("连接失败！")
            return None

    except mysql.connector.Error as e:
        print(f"发生错误：{e}")
        return None
def check_production_line(df, column_name, production_lines):
    values = df[column_name].unique()
    for value in values:
        if value in production_lines:
            return True
    return False

def compare_headers(expected_headers, uploaded_headers):
    return expected_headers == uploaded_headers

def extract_from_excel(file_path):
    # 读取Excel文件
    df = pd.read_excel(file_path)

    nested_array = df.values.tolist()

    return nested_array

def insert_data_to_mysql(data, table):
    try:
        # 连接 MySQL 数据库
        conn = connect_to_database()
        cursor = conn.cursor()

        # 校验数据是否为空
        if not data:
            print("要插入的数据为空。")
            return

        # 校验数据格式并获取列数
        num_columns = len(data[0])
        for row in data:
            if len(row) != num_columns:
                print("数据行长度与目标表的列数不匹配。")
                return

        # 将空值替换为 None
        data_with_none = [[None if pd.isnull(value) else value for value in row] for row in data]

        # 插入数据到表中
        placeholders = ', '.join(['%s'] * num_columns)
        query = f"INSERT INTO {table} VALUES ({placeholders})"
        cursor.executemany(query, data_with_none)

        # 提交事务
        conn.commit()
        print("数据已成功插入到数据库表中。")

    except mysql.connector.Error as err:
        print("MySQL 错误:", err)
        conn.rollback()  # 回滚事务以撤销之前的操作

    finally:
        # 关闭连接
        cursor.close()
        conn.close()

def query_rows_by_ids(ids, table):
    # 建立数据库连接
    conn = connect_to_database()

    try:
        # 创建游标对象
        cursor = conn.cursor()

        # 构建 SQL 查询语句，并使用参数占位符来传递表名和 id 数组
        sql = f"SELECT * FROM {table} WHERE id IN ({', '.join(['%s'] * len(ids))})"

        # 执行 SQL 语句，传递 id 数组作为参数
        cursor.execute(sql, tuple(ids))

        # 获取查询结果
        rows = cursor.fetchall()

        # 将查询结果转换为数组形式输出
        result = []
        for row in rows:
            result.append(list(row))

        return result

    except mysql.connector.Error as error:
        # 处理查询失败的情况
        print("查询数据行时出现错误:", error)

    finally:
        # 关闭游标和数据库连接
        if cursor:
            cursor.close()
        if conn.is_connected():
            conn.close()
def query_range(table,seleceted_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    query = f"SELECT * FROM {table} WHERE id = %s"
    cursor.execute(query, (seleceted_id,))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    min = data[0][1]
    max = data[0][2]
    return min, max


def query_data_in_range(table, column, min_value, max_value, page, page_size):
    # 连接到MySQL数据库
    conn = connect_to_database()
    # 创建游标对象
    cursor = conn.cursor()

    try:
        offset = (page - 1) * page_size
        query = f"SELECT * FROM {table} WHERE {column} >= %s AND {column} < %s LIMIT %s OFFSET %s"
        cursor.execute(query, (min_value, max_value, page_size, offset))

        # 获取查询结果
        results = cursor.fetchall()

        # 获取满足条件的总行数
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
def update_row_numbers(table):
    conn = connect_to_database()
    cursor = conn.cursor()

    # 获取表数据
    select_query = f"SELECT * FROM {table}"
    cursor.execute(select_query)
    rows = cursor.fetchall()

    # 更新表数据
    update_query = f"UPDATE {table} SET id = %s WHERE id = %s"
    for i, row in enumerate(rows):
        row_id = row[0]
        cursor.execute(update_query, (i+1, row_id))

    # 提交事务并关闭连接
    conn.commit()
    cursor.close()
    conn.close()
def delete_rows_by_ids(ids,table):
    # 建立数据库连接
    conn = connect_to_database()

    try:
        # 创建游标对象
        cursor = conn.cursor()

        # 构建 SQL 删除语句，并使用参数占位符来传递表名和 id 数组
        sql = f"DELETE FROM {table} WHERE id IN ({', '.join(['%s'] * len(ids))})"

        # 执行 SQL 语句，传递 id 数组作为参数
        cursor.execute(sql, tuple(ids))

        # 提交事务
        conn.commit()

        update_row_numbers(table)

    except mysql.connector.Error as error:
        # 处理删除失败的情况
        print("删除数据行时出现错误:", error)

    finally:
        # 关闭游标和数据库连接
        if cursor:
            cursor.close()
        if conn.is_connected():
            conn.close()

def edit_rows_by_ids(ids, nested_data, column_names,table):
    conn = connect_to_database()
    cursor = conn.cursor()

    # 构建更新语句
    update_query = f"UPDATE {table} SET {{}} = %s WHERE id = %s"

    for id_value in ids:
        # 获取要更新的数据
        nested_row_index = None
        for index, row in enumerate(nested_data):
            if row[0] == id_value:
                nested_row_index = index
                break

        if nested_row_index is not None:
            nested_row = nested_data[nested_row_index]

            # 更新每个列
            for i, column_name in enumerate(column_names):
                update_statement = update_query.format(column_name)
                cursor.execute(update_statement, (nested_row[i], id_value))

    # 提交事务并关闭连接
    conn.commit()
    cursor.close()
    conn.close()



def split_string(input_string):
    # 使用 split() 方法按照 '-' 进行分割
    parts = input_string.split('-')
    return parts
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
def fetch_data_from_mysql(column, value, select_columns, key_column):
    # 连接到MySQL数据库（用你的实现替换connect_to_database）
    conn = connect_to_database()
    cursor = conn.cursor()

    try:
        # 将select_columns转换为逗号分隔的字符串
        select_columns_str = ', '.join(select_columns)

        # 执行SQL查询
        query = f"SELECT {key_column}, {select_columns_str} FROM modelist WHERE {column} = %s"
        cursor.execute(query, (value,))

        # 检索查询结果
        result = cursor.fetchall()
        data_dict = {}

        if result:
            # 用键-值对填充字典，并将值存入数组
            for row in result:
                key_value = row[0]  # 假设第一列是键
                values = row[1:]
                data_dict[key_value] = dict(zip(select_columns, values))
                values_array = list(data_dict.values())
                values_dict = values_array[0]
                value_value = []
                for value_dict in values_array:
                    value_value.extend(value_dict.values())
        else:
            print("未找到匹配记录.")

        return select_columns, values_dict, value_value

    except mysql.connector.Error as e:
        print(f"错误: {e}")

def update_mysql_data(data_array, fixed_field):
    # 连接到 MySQL 数据库
    conn = connect_to_database()

    try:
        with conn.cursor() as cursor:
            # 遍历数据数组中的每一个键值对
            for item in data_array:
                # 构造 SQL 更新语句
                sql = f"UPDATE modelist SET "
                for key, value in item.items():
                    if key != fixed_field:
                        sql += f"{key} = '{value}', "
                sql = sql[:-2]  # 去掉末尾的逗号和空格
                sql += f" WHERE {fixed_field} = '{item[fixed_field]}'"

                # 执行 SQL 更新语句
                cursor.execute(sql)

        # 提交事务
        conn.commit()

    finally:
        # 关闭数据库连接
        conn.close()

###
@app.route('/send_submenu', methods=['POST'])
def send_submenu():
    try:
        data = request.get_json()
        global current_page, local_current_pageNumber
        current_page = data.get('currentPage')
        local_current_pageNumber = data.get('localCurrentPageNumber')
        return jsonify({'currentPage': current_page, 'localCurrentPageNumber': local_current_pageNumber})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/send_items_per_page', methods=['POST'])
def send_items_per_page():
    try:
        data = request.get_json()
        items_per_page = data.get('itemsPerPage')
        # 根据当前页和每页项数计算起始和结束索引
        start_index = (local_current_pageNumber - 1) * items_per_page
        end_index = start_index + items_per_page
        label = split_string(current_page)[0]
        pline = split_string(current_page)[1]
        result = extract_data('标签', label, '所属产线', pline, ['序号','模型名称（中文）', '模型名称（英文）', '运行语言', '标签'], key_mapping)
        print(result)
        result_list = list(result.values())
        paginated_result = result_list[start_index:end_index]

        if paginated_result is not None and paginated_result:
            print(f"'标签' 列与 '{current_page}' 相同的数据行的选择列：")
            print(paginated_result)
        else:
            print(f"'标签' 列与 '{current_page}' 相同的数据行不存在或选择失败.")
        return jsonify({'data': paginated_result, 'totalPages': len(result) // items_per_page + 1})

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/getTableData', methods=['POST'])
def get_table_data():
    data = request.get_json()
    global chinese_name
    chinese_name = data.get('chineseName')
    print(chinese_name)
    table_one = fetch_data_from_mysql('模型名称（中文）', chinese_name, ['模型名称（英文）', '所属产线'], '序号')[1]
    table_two = fetch_data_from_mysql('模型名称（中文）', chinese_name, ['运行语言', '所属工序'], '序号')[1]
    table_three = fetch_data_from_mysql('模型名称（中文）', chinese_name, ['参数描述'], '序号')[1]
    table_four = fetch_data_from_mysql('模型名称（中文）', chinese_name, ['测试代码'], '序号')[1]
    inbound_time = fetch_data_from_mysql('模型名称（中文）', chinese_name, ['入库时间'], '序号')[1]['入库时间']
    test_code = fetch_data_from_mysql('模型名称（中文）', chinese_name, ['测试代码'], '序号')[1]['测试代码']
    return jsonify({'tableOne': table_one, 'tableTwo': table_two, 'tableThree': table_three, 'tableFour': table_four,
                    'inboundTime': inbound_time, 'testCode': test_code})

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    req_data = data.get('inputData')
    data = json.loads(req_data)
    url = fetch_data_from_mysql('模型名称（中文）', chinese_name, ['API'], '序号')[1]['API']
    headers = {"Content-Type": "application/json;charset=UTF-8"}
    result = requests.post(url=url, data=json.dumps(data), headers=headers, verify=False)
    resp_data = json.loads(result.text)["resp_data"]
    resp_data = list(resp_data.values())
    return jsonify(resp_data)
@app.route('/send_list', methods=['POST'])
def send_list():
    try:
        data = request.get_json()
        selected_label = data.get('selectedLabel')
        model_list = fetch_data_from_mysql('标签', selected_label, ['模型名称（中文）'], '序号')[2]
        return jsonify({'modelList': model_list})
    except Exception as e:
        return jsonify({'error': str(e)})
@app.route('/get_model_data', methods=['POST'])
def get_model_data():
    data = request.get_json()
    selected_model = data.get('selectedModel')
    models_data = []
    key = fetch_data_from_mysql('模型名称（中文）', selected_model[0], ['模型名称（中文）', '所属产线', '所属工序', '入库时间'], '序号')[0]
    for model in selected_model:
        model_data = fetch_data_from_mysql('模型名称（中文）', model, ['模型名称（中文）', '所属产线', '所属工序', '入库时间'], '序号')[1]
        models_data.append(model_data)
    return jsonify({'modelData': models_data, 'Key': key})
@app.route('/send_edit', methods=['POST'])
def send_edit():
    try:
        data = request.get_json()
        model_data = data.get('modelData')
        update_mysql_data(model_data, '模型名称（中文）')
        return jsonify({'message': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    # app.run(
    #     host='192.168.151.199',
    #     port=9999,
    #     debug=True
    # )
    app.run(
        host='0.0.0.0',
        port=60000,
        debug=True
    )