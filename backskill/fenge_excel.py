# _*_ coding: utf-8 _*_
# @File:    fenge_excel
# @Time:    2024/3/25 9:54
# @Author:  chenxuejiao
# @Contact: 15801102378@163.com
# @Version: V 0.1

import pandas as pd

def split_excel_by_rows(input_excel_file, output_prefix, rows_per_file):
    # 读取原始 Excel 文件
    df = pd.read_excel(input_excel_file)

    # 计算分割后的文件数
    num_files = -(-len(df) // rows_per_file)  # Ceiling division

    # 分割数据并保存到多个 Excel 文件中
    for i in range(num_files):
        start_index = i * rows_per_file
        end_index = min((i + 1) * rows_per_file, len(df))
        output_file = f"{output_prefix}_{i + 1}.xlsx"
        df.iloc[start_index:end_index].to_excel(output_file, index=False)


# 示例用法
input_excel_file = "shengyang1700.xlsx"  # 输入的 Excel 文件名
output_prefix = "shengyang"  # 输出文件的前缀
rows_per_file = 5000  # 每个输出文件的行数

split_excel_by_rows(input_excel_file, output_prefix, rows_per_file)
