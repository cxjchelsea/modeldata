import json

from flask import Flask, jsonify
from flask_cors import CORS
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
def get_parameter_information(table_name, model_name):
    try:
        # 连接到 MySQL 数据库
        connection = connect_to_database()

        if connection.is_connected():
            # 创建游标对象
            cursor = connection.cursor()

            # 执行查询
            query = f"SELECT `参数描述` FROM `{table_name}` WHERE `模型名称（中文）` = %s"
            cursor.execute(query, (model_name,))
            describe = cursor.fetchone()[0]
            query = f"SELECT `测试代码` FROM `{table_name}` WHERE `模型名称（中文）` = %s"
            cursor.execute(query, (model_name,))
            code = cursor.fetchone()[0]
            query = f"SELECT `参数类型` FROM `{table_name}` WHERE `模型名称（中文）` = %s"
            cursor.execute(query, (model_name,))
            type = cursor.fetchone()[0]
            # 关闭游标和连接
            cursor.close()
            connection.close()

            return describe, code, type
        else:
            print("连接失败！")
            return None

    except mysql.connector.Error as e:
        print(f"发生错误：{e}")
        return None
def create_tip(table_name, model_name, para_type, para_describe, key_value, key_dict):
    connection = connect_to_database()
    cursor = connection.cursor()
    query = f"SELECT `模型名称（英文）` FROM `{table_name}` WHERE `模型名称（中文）` = %s"
    cursor.execute(query, (model_name,))
    model_english = cursor.fetchone()[0]
    # 关闭游标和连接
    cursor.close()
    connection.close()
    template = f"""
# 动态库的导入
# 导入python的外部函数库ctypes提供与C兼容的数据类型以调用DLL。
# 将动态库dll文件的绝对路径赋给dll_path（直接替换path/to/your/dll）

import ctypes
dll_path = path/to/your/dll
model = ctypes.CDLL(dll_path)


# 模型函数的定义
# 根据函数自动生成参数定义。

model.{model_english}.argtypes = {para_type}
model.{model_english}.restype = {para_type[0]}


# 输入参数的赋值
# 此处根据需要给模型的输入参数赋值，替换模板中的输入变量的值。
{para_describe}

{key_value}


# 结果计算

result = model.{model_english}{key_dict}
# print(result)
    """
    return template

app = Flask(__name__)
CORS(app)

@app.route('/generate_code', methods=['GET'])
def generate_code():
    para_describe, code, para_type = get_parameter_information('modelist', 'WeathResiStl_DefRes')
    array = [type.strip() for type in para_type.split(',')]
    para_type = [f"ctypes.c_{type}" for type in array]
    para = json.loads(code)
    req_data = para["req_data"]
    key_value = ", ".join(f"{key}={value}" for key, value in req_data.items())
    key_dict = f"({', '.join(req_data.keys())})"
    template = create_tip('WeathResiStl_DefRes', para_type, para_describe, key_value, key_dict)

    return jsonify(template)

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=60000,
        debug=True
    )
