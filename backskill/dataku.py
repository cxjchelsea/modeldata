# _*_ coding: utf-8 _*_
# @File:    dataku
# @Time:    2024/4/15 15:05
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
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Invalid username or password'}), 400

    user = next((user for user in users if user['username'] == username and user['password'] == password), None)

    if user:
        return jsonify({'message': 'Login successful', 'role': user['role']}), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401


@app.route('/get_line_data', methods=['GET'])
def get_line_header():
    try:
        line_data_count = get_row_count("information_roll_line")
        conn = connect_to_database()

        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SHOW COLUMNS FROM information_roll_line")
        table_header = [column[0] for column in cursor.fetchall()]
        cursor.close()

        cursor = conn.cursor()
        data_query = "SELECT * FROM information_roll_line"
        cursor.execute(data_query)
        table_data = cursor.fetchall()
        cursor.close()

        cursor = conn.cursor()
        query = "SELECT 序号名称 FROM information_roll_line"
        cursor.execute(query)
        data = [row[0] for row in cursor.fetchall()]
        selected_line_options = list(set(data))
        cursor.close()

        cursor = conn.cursor()
        query = "SELECT 工厂设计 FROM information_roll_line"
        cursor.execute(query)
        data = [row[0] for row in cursor.fetchall()]
        selected_design_options = list(set(data))
        cursor.close()
        conn.close()
        return jsonify({'LineDataCount': line_data_count, 'tableHeader': table_header, 'tableData': table_data, 'selectedLineOptions': selected_line_options, 'selectedDesignOptions': selected_design_options})
    except Exception as e:
        print(f"Error fetching table data: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/send_selected_line', methods=['POST'])
def send_selected_line():
    try:
        data = request.get_json()
        selected_line = data.get('selectedLine')
        conn = connect_to_database()
        cursor = conn.cursor()
        query = "SELECT * FROM information_roll_line WHERE 序号名称 = %s"
        cursor.execute(query, (selected_line,))
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)})
@app.route('/send_selected_design', methods=['POST'])
def send_selected_design():
    try:
        data = request.get_json()
        selected_design = data.get('selectedDesign')
        conn = connect_to_database()
        cursor = conn.cursor()
        query = "SELECT * FROM information_roll_line WHERE 工厂设计 = %s"
        cursor.execute(query, (selected_design,))
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)})
@app.route('/send_selected_year', methods=['POST'])
def send_selected_year():
    try:
        data = request.get_json()
        selected_year = data.get('selectedYear')
        conn = connect_to_database()
        cursor = conn.cursor()
        query = "SELECT * FROM information_roll_line WHERE 投产时间 LIKE %s"
        cursor.execute(query, (f'{selected_year}%',))
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/upload_line', methods=['POST'])
def upload_line():
    if 'file' not in request.files:
        return jsonify({'error': '没有上传文件'})

    files = request.files.getlist('file')

    if not files:
        return jsonify({'error': '上传文件为空'})

    expected_headers = get_table_columns('information_roll_line')

    uploaded_files = []  # 用于存储上传成功的文件名
    mismatched_files = []  # 用于存储表头不一致的文件名
    existing_production_files = []  # 用于存储已存在于产线名称数组中的文件名
    production_lines = get_column_data('PlantName', 'information_roll_line')

    # 连接 MySQL 数据库
    conn = connect_to_database()
    cursor = conn.cursor()

    for file in files:
        filename = file.filename

        # 使用 pandas 读取 Excel 文件并获取表头
        df = pd.read_excel(file)
        uploaded_headers = df.columns.tolist()

        if compare_headers(expected_headers, uploaded_headers):
            # 检查是否存在于产线名称数组中
            if check_production_line(df, 'PlantName', production_lines):
                existing_production_files.append(filename)
            else:
                table_data = extract_from_excel(file)

                insert_data_to_mysql(table_data, 'information_roll_line')
                update_row_numbers('information_roll_line')
                uploaded_files.append(filename)
        else:
            mismatched_files.append(filename)

    data_query = "SELECT * FROM information_roll_line"
    cursor.execute(data_query)
    table_data = cursor.fetchall()
    # 关闭 MySQL 连接
    cursor.close()
    conn.close()

    return jsonify({'beingUpload': uploaded_files, 'mismatchUpload': mismatched_files,
                    'existUpload': existing_production_files,'tableData': table_data})

@app.route('/select_lines', methods=['POST'])
def select_lines():
    try:
        data = request.get_json()
        selected_rows_ids = data.get('selectedRowsIds')
        selected_data = query_rows_by_ids(selected_rows_ids, 'information_roll_line')
        return jsonify({'selectedData': selected_data})
    except Exception as e:
        print(f"Error delete table data: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/delete_lines', methods=['POST'])
def delete_lines():
    try:
        data = request.get_json()
        selected_rows_ids = data.get('selectedRowsIds')
        delete_rows_by_ids(selected_rows_ids, 'information_roll_line')
        conn = connect_to_database()
        cursor = conn.cursor()
        data_query = "SELECT * FROM information_roll_line"
        cursor.execute(data_query)
        table_data = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({'tableData': table_data})
    except Exception as e:
        print(f"Error delete table data: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/edit_lines', methods=['POST'])
def edit_lines():
    try:
        data = request.get_json()
        selected_rows_ids = data.get('selectedRowsIds')
        update_data = data.get('updateData')
        edit_rows_by_ids(selected_rows_ids, update_data, columns, 'information_roll_line')
        conn = connect_to_database()
        cursor = conn.cursor()
        data_query = "SELECT * FROM information_roll_line"
        cursor.execute(data_query)
        table_data = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({'tableData': table_data})
    except Exception as e:
        print(f"Error delete table data: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
@app.route('/edit_header', methods=['POST'])
def edit_header():
    try:
        data = request.get_json()
        update_header = data.get('updateHeader')
        modify_table_headers('information_roll_line', update_header)
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SHOW COLUMNS FROM information_roll_line")
        table_header = [column[0] for column in cursor.fetchall()]
        cursor.close()
        conn.close()
        return jsonify({'tableHeader': table_header})
    except Exception as e:
        print(f"Error delete table data: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
###
@app.route('/get_material_data', methods=['GET'])
def get_material_header():
    try:
        material_data_count = get_row_count("material_data")
        conn = connect_to_database()

        cursor = conn.cursor()
        header_query = "SELECT chinese_name FROM material_data_name_with_id"
        cursor.execute(header_query)
        table_header = [row[0] for row in cursor.fetchall()]
        cursor.close()

        cursor = conn.cursor()
        query = "SELECT english_name FROM material_data_name_with_id"
        cursor.execute(query)
        global columns
        columns = [row[0] for row in cursor.fetchall()]
        cursor.close()

        cursor = conn.cursor()
        data_query = "SELECT * FROM material_data"
        cursor.execute(data_query)
        table_data = cursor.fetchall()
        cursor.close()

        cursor = conn.cursor()
        query = "SELECT Type FROM material_data"
        cursor.execute(query)
        data = [row[0] for row in cursor.fetchall()]
        selected_type_options = list(set(data))
        cursor.close()

        cursor = conn.cursor()
        query = "SELECT Type1 FROM material_data"
        cursor.execute(query)
        data = [row[0] for row in cursor.fetchall()]
        selected_type1_options = list(set(data))
        cursor.close()

        cursor = conn.cursor()
        query = "SELECT Type2 FROM material_data"
        cursor.execute(query)
        data = [row[0] for row in cursor.fetchall()]
        selected_type2_options = list(set(data))
        cursor.close()

        cursor = conn.cursor()
        query = "SELECT Grade FROM material_data"
        cursor.execute(query)
        data = [row[0] for row in cursor.fetchall()]
        selected_grade_options = list(set(data))
        cursor.close()


        conn.close()
        return jsonify({'MaterialDataCount': material_data_count, 'tableHeader': table_header, 'tableData': table_data, 'selectedTypeOptions': selected_type_options, 'selectedType1Options': selected_type1_options, 'selectedType2Options': selected_type2_options, 'selectedGradeOptions': selected_grade_options})
    except Exception as e:
        print(f"Error fetching table data: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/send_selected_type', methods=['POST'])
def send_selected_type():
    try:
        data = request.get_json()
        selected_type = data.get('selectedType')
        conn = connect_to_database()
        cursor = conn.cursor()
        query = "SELECT * FROM material_data WHERE Type = %s"
        cursor.execute(query, (selected_type,))
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/send_selected_type1', methods=['POST'])
def send_selected_type1():
    try:
        data = request.get_json()
        selected_type1 = data.get('selectedType1')
        conn = connect_to_database()
        cursor = conn.cursor()
        query = "SELECT * FROM material_data WHERE Type1 = %s"
        cursor.execute(query, (selected_type1,))
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/send_selected_type2', methods=['POST'])
def send_selected_type2():
    try:
        data = request.get_json()
        selected_type2 = data.get('selectedType2')
        conn = connect_to_database()
        cursor = conn.cursor()
        query = "SELECT * FROM material_data WHERE Type2 = %s"
        cursor.execute(query, (selected_type2,))
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/send_selected_grade', methods=['POST'])
def send_selected_grade():
    try:
        data = request.get_json()
        selected_grade = data.get('selectedGrade')
        conn = connect_to_database()
        cursor = conn.cursor()
        query = "SELECT * FROM material_data WHERE Grade = %s"
        cursor.execute(query, (selected_grade,))
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/upload_material', methods=['POST'])
def upload_material():
    if 'file' not in request.files:
        return jsonify({'error': '没有上传文件'})

    files = request.files.getlist('file')

    if not files:
        return jsonify({'error': '上传文件为空'})

    expected_headers = get_table_columns('material_data')

    uploaded_files = []  # 用于存储上传成功的文件名
    mismatched_files = []  # 用于存储表头不一致的文件名
    existing_production_files = []  # 用于存储已存在于产线名称数组中的文件名
    material_grade = get_column_data('Grade', 'material_data')

    # 连接 MySQL 数据库
    conn = connect_to_database()
    cursor = conn.cursor()

    for file in files:
        filename = file.filename

        # 使用 pandas 读取 Excel 文件并获取表头
        df = pd.read_excel(file)
        uploaded_headers = df.columns.tolist()

        if compare_headers(expected_headers, uploaded_headers):
            # 检查是否存在于产线名称数组中
            if check_production_line(df, 'Grade', material_grade):
                existing_production_files.append(filename)
            else:
                table_data = extract_from_excel(file)
                insert_data_to_mysql(table_data, 'material_data')
                update_row_numbers('material_data')
                uploaded_files.append(filename)
        else:
            mismatched_files.append(filename)

    data_query = "SELECT * FROM material_data"
    cursor.execute(data_query)
    table_data = cursor.fetchall()
    # 关闭 MySQL 连接
    cursor.close()
    conn.close()

    return jsonify({'beingUpload': uploaded_files, 'mismatchUpload': mismatched_files,
                    'existUpload': existing_production_files,'tableData': table_data})

@app.route('/select_materials', methods=['POST'])
def select_materials():
    try:
        data = request.get_json()
        selected_rows_ids = data.get('selectedRowsIds')
        selected_data = query_rows_by_ids(selected_rows_ids, 'material_data')
        return jsonify({'selectedData': selected_data})
    except Exception as e:
        print(f"Error delete table data: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/delete_materials', methods=['POST'])
def delete_materials():
    try:
        data = request.get_json()
        selected_rows_ids = data.get('selectedRowsIds')
        delete_rows_by_ids(selected_rows_ids, 'material_data')
        conn = connect_to_database()
        cursor = conn.cursor()
        data_query = "SELECT * FROM material_data"
        cursor.execute(data_query)
        table_data = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({'tableData': table_data})
    except Exception as e:
        print(f"Error delete table data: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/edit_materials', methods=['POST'])
def edit_materials():
    try:
        data = request.get_json()
        selected_rows_ids = data.get('selectedRowsIds')
        update_data = data.get('updateData')
        print(selected_rows_ids)
        print(update_data)
        edit_rows_by_ids(selected_rows_ids, update_data, columns, 'material_data')
        conn = connect_to_database()
        cursor = conn.cursor()
        data_query = "SELECT * FROM material_data"
        cursor.execute(data_query)
        table_data = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({'tableData': table_data})
    except Exception as e:
        print(f"Error delete table data: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
###
@app.route('/get_product_data', methods=['GET'])
def get_product_data():
    try:
        product_line_count = get_row_count('product_roll_line_name')
        conn = connect_to_database()
        cursor = conn.cursor()
        query = "SELECT roll_line, line_number FROM product_roll_line_name"
        cursor.execute(query)
        product_line_data = {row[0]: row[1] for row in cursor.fetchall()}
        total_product_line_data = sum(product_line_data.values())
        conn = connect_to_database()
        cursor = conn.cursor()
        roll_line_query = f"SELECT * FROM product_roll_line_name"
        cursor.execute(roll_line_query)
        roll_line = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return jsonify({'ProductLineCount': product_line_count, 'TotalProductLineData': total_product_line_data, 'ProductLineData': product_line_data, 'selectedPlineOptions': roll_line})
    except Exception as e:
        print(f"Error fetching table data: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/send_selected_pline', methods=['POST'])
def send_selected_pline():
    try:
        data = request.get_json()
        global selected_pline
        selected_pline = data.get('selectedPline')
        page = data.get('page')
        page_size = data.get('pageSize')
        offset = (page - 1) * page_size
        conn = connect_to_database()
        cursor = conn.cursor()
        select_product_line_count = get_row_count(selected_pline)
        header_query = f"SELECT chinese_name FROM {selected_pline}_name_with_id"
        cursor.execute(header_query)
        table_header = [row[0] for row in cursor.fetchall()]
        count_query = f"SELECT COUNT(*) FROM {selected_pline}"
        cursor.execute(count_query)
        total_rows = cursor.fetchone()[0]
        data_query = f"SELECT * FROM {selected_pline} LIMIT %s OFFSET %s"
        cursor.execute(data_query, (page_size, offset))
        table_data = cursor.fetchall()
        grade_query = f"SELECT Grade_name FROM {selected_pline}"
        cursor.execute(grade_query)
        data = [row[0] for row in cursor.fetchall()]
        selected_grade_name_options = list(set(data))
        width_query = f"SELECT * FROM width"
        cursor.execute(width_query)
        selected_width_options = cursor.fetchall()
        thick_query = f"SELECT * FROM thick"
        cursor.execute(thick_query)
        selected_thick_options = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({'SelectProductLineCount': select_product_line_count, 'tableHeader': table_header, 'tableData': table_data, 'totalRows': total_rows, 'selectedGradenameOptions': selected_grade_name_options, 'selectedWidthOptions': selected_width_options, 'selectedThickOptions': selected_thick_options})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/send_selected_grade_name', methods=['POST'])
def send_selected_grade_name():
    try:
        data = request.get_json()
        selected_grade_name = data.get('selectedGradename')
        page = data.get('page')
        page_size = data.get('pageSize')
        conn = connect_to_database()
        cursor = conn.cursor()
        offset = (page - 1) * page_size
        query = f"SELECT * FROM {selected_pline} WHERE Grade_name = %s LIMIT %s OFFSET %s"
        cursor.execute(query, (selected_grade_name, page_size, offset))
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        conn = connect_to_database()
        cursor = conn.cursor()
        count_query = f"SELECT COUNT(*) FROM {selected_pline} WHERE Grade_name = %s"
        cursor.execute(count_query, (selected_grade_name,))
        total_rows = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        total_pages = math.ceil(total_rows / page_size)

        return jsonify({'Data': data, 'totalPages': total_pages})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/send_selected_time', methods=['POST'])
def send_selected_time():
    try:
        data = request.get_json()
        selected_time = data.get('selectedDate')
        page = data.get('page')
        page_size = data.get('pageSize')
        conn = connect_to_database()
        cursor = conn.cursor()
        offset = (page - 1) * page_size
        query = f"SELECT * FROM {selected_pline} WHERE DATE (S_Time) = %s LIMIT %s OFFSET %s"
        cursor.execute(query, (selected_time, page_size, offset))
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        conn = connect_to_database()
        cursor = conn.cursor()
        count_query = f"SELECT COUNT(*) FROM {selected_pline} WHERE DATE (S_Time) = %s"
        cursor.execute(count_query, (selected_time,))
        total_rows = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        total_pages = math.ceil(total_rows / page_size)

        return jsonify({'Data': data, 'totalPages': total_pages})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/send_selected_width', methods=['POST'])
def send_selected_width():
    try:
        data = request.get_json()
        selected_width = data.get('selectedWidth')
        min_width, max_width = query_range('width', selected_width)
        page = data.get('page')
        page_size = data.get('pageSize')
        result = query_data_in_range(selected_pline, 'S_Wid', min_width, max_width, page, page_size)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)})
@app.route('/send_selected_thick', methods=['POST'])
def send_selected_thick():
    try:
        data = request.get_json()
        selected_thick = data.get('selectedThick')
        min_thick, max_thick = query_range('thick', selected_thick)
        page = data.get('page')
        page_size = data.get('pageSize')
        result = query_data_in_range(selected_pline, 'S_Thick', min_thick, max_thick, page, page_size)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/upload_product', methods=['POST'])
def upload_product():
    if 'file' not in request.files:
        return jsonify({'error': '没有上传文件'})

    files = request.files.getlist('file')

    if not files:
        return jsonify({'error': '上传文件为空'})

    expected_headers = get_table_columns(selected_pline)

    uploaded_files = []  # 用于存储上传成功的文件名
    mismatched_files = []  # 用于存储表头不一致的文件名
    existing_production_files = []  # 用于存储已存在于产线名称数组中的文件名
    production_lines = get_column_data('Coil_ID', selected_pline)

    # 连接 MySQL 数据库
    conn = connect_to_database()
    cursor = conn.cursor()

    for file in files:
        filename = file.filename

        # 使用 pandas 读取 Excel 文件并获取表头
        df = pd.read_excel(file)
        uploaded_headers = df.columns.tolist()

        if compare_headers(expected_headers, uploaded_headers):
            # 检查是否存在于产线名称数组中
            if check_production_line(df, 'Coil_ID', production_lines):
                existing_production_files.append(filename)
            else:
                table_data = extract_from_excel(file)
                insert_data_to_mysql(table_data, selected_pline)
                update_row_numbers(selected_pline)
                uploaded_files.append(filename)
        else:
            mismatched_files.append(filename)

    data_query = f"SELECT * FROM {selected_pline}"
    cursor.execute(data_query)
    table_data = cursor.fetchall()
    # 关闭 MySQL 连接
    cursor.close()
    conn.close()

    return jsonify({'beingUpload': uploaded_files, 'mismatchUpload': mismatched_files,
                    'existUpload': existing_production_files,'tableData': table_data})

@app.route('/select_products', methods=['POST'])
def select_products():
    try:
        data = request.get_json()
        selected_rows_ids = data.get('selectedRowsIds')
        selected_data = query_rows_by_ids(selected_rows_ids, selected_pline)
        return jsonify({'selectedData': selected_data})
    except Exception as e:
        print(f"Error delete table data: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/delete_products', methods=['POST'])
def delete_products():
    try:
        data = request.get_json()
        selected_rows_ids = data.get('selectedRowsIds')
        delete_rows_by_ids(selected_rows_ids, selected_pline)
        conn = connect_to_database()
        cursor = conn.cursor()
        data_query = f"SELECT * FROM {selected_pline}"
        cursor.execute(data_query)
        table_data = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({'tableData': table_data})
    except Exception as e:
        print(f"Error delete table data: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500


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