import os
import re
import pandas as pd
import shutil

def extract_function_signatures(directory):
    # 获取所有 .cpp 文件
    cpp_files = [f for f in os.listdir(directory) if f.endswith('.cpp')]
    functions_info = {}

    # 正则表达式匹配函数声明
    func_pattern = re.compile(r'\b([a-zA-Z_]\w*)\s+([a-zA-Z_]\w*)\s*\(([^)]*)\)')

    for cpp_file in cpp_files:
        file_name_without_ext = os.path.splitext(cpp_file)[0]
        functions_info[file_name_without_ext] = []
        with open(os.path.join(directory, cpp_file), 'r', encoding='latin-1') as file:
            content = file.read()
            matches = func_pattern.findall(content)
            for match in matches:
                return_type = match[0]
                func_name = match[1]
                params = match[2].split(',') if match[2] else []
                param_types = [param.strip().split()[0] for param in params if param.strip()]
                functions_info[file_name_without_ext].append((func_name, param_types))

    return functions_info


def save_to_excel(data, output_file):
    # 创建一个 DataFrame
    rows = []
    for file_name, functions in data.items():
        for func_name, param_types in functions:
            rows.append([file_name, func_name, ', '.join(param_types)])

    df = pd.DataFrame(rows, columns=['File Name', 'Function Name', 'Parameter Types'])

    # 将 DataFrame 保存为 Excel 文件
    df.to_excel(output_file, index=False)


# 调用函数并保存结果到 Excel 文件
directory = './cpp'
output_file = 'function_signatures.xlsx'

function_signatures = extract_function_signatures(directory)
save_to_excel(function_signatures, output_file)

print(f"Function signatures have been saved to {output_file}")
