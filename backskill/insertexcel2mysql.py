import pandas as pd
import mysql.connector
import re
import os
def insert_data_to_table(df, table_name):
    try:
        # 连接到 MySQL 数据库
        connection = mysql.connector.connect(
            host='localhost',
            database='test',
            user='root',
            password='123456',
            auth_plugin='mysql_native_password'
        )

        # 创建一个 MySQL 游标
        cursor = connection.cursor()

        df = df.astype(object).where(pd.notnull(df), None)
        for index, row in df.iterrows():
            insert_values = tuple(row)
            insert_query = f"INSERT INTO {table_name} ({', '.join([f'`{col}`' for col in df.columns])}) VALUES ({', '.join(['%s'] * len(df.columns))})"
            cursor.execute(insert_query, insert_values)


        # 提交更改
        connection.commit()

        # 关闭游标和连接
        cursor.close()
        connection.close()

        print("数据已成功插入到 MySQL 数据库表中。")

    except mysql.connector.Error as err:
        print("MySQL 错误:", err)

# 读取 Excel 文件
excel_file = "E:\\1Study&Work\modeldata\数据存档\模型库\modelist.xlsx"  # 替换为你的 Excel 文件路径
df = pd.read_excel(excel_file)
table_name = 'modelist'
# 调用函数插入数据到表格中
insert_data_to_table(df, table_name)


# 函数：修正列名
# def remove_special_characters(column):
#     # 使用正则表达式去掉特殊字符
#     column = re.sub(r'[^\w\s]', '', column)
#     return column.strip()  # 去掉首尾空格
#
# # 函数：将数据插入到表格中
# def insert_data_to_table(df):
#     try:
#         # 连接到 MySQL 数据库
#         connection = mysql.connector.connect(
#             host='localhost',
#             database='test',
#             user='root',
#             password='123456',
#             auth_plugin='mysql_native_password'
#         )
#
#         # 创建一个 MySQL 游标
#         cursor = connection.cursor()
#
#         # 处理空值，将 NaN 转换为 None
#         df = df.astype(object).where(pd.notnull(df), None)
#
#         for index, row in df.iterrows():
#             insert_values = tuple(row)
#             insert_query = f"INSERT INTO qiangang2160 ({', '.join([f'`{col}`' for col in df.columns])}) VALUES ({', '.join(['%s'] * len(df.columns))})"
#             cursor.execute(insert_query, insert_values)
#
#         # 提交更改
#         connection.commit()
#
#         # 关闭游标和连接
#         cursor.close()
#         connection.close()
#
#         print("数据已成功插入到 MySQL 数据库表中。")
#
#     except mysql.connector.Error as err:
#         print("MySQL 错误:", err)
#
# # 获取指定文件夹中的所有CSV文件
# folder_path = "2160"  # 替换为你的文件夹路径
# csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
#
# # 遍历所有CSV文件并逐个插入数据
# for csv_file in csv_files:
#     file_path = os.path.join(folder_path, csv_file)
#     # 读取 CSV 文件并处理列名
#     df = pd.read_csv(file_path, header=0)
#     df.columns = [remove_special_characters(name) for name in df.columns]
#
#     # 调用函数插入数据到表格中
#     insert_data_to_table(df)

# # 读取 CSV 文件
# df = pd.read_csv("H21.202204.csv")
#
# # 获取实测CT温度H21_0列的实际长度
# lengths = df['实测CT温度(H21_0)'].str.len()
#
# # 打印最大长度
# print("最大长度:", lengths.max())
#
# # 打印最小长度
# print("最小长度:", lengths.min())
#
# # 打印长度的统计信息
# print("长度统计信息:", lengths.describe())
