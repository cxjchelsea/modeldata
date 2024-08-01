import mysql.connector


def edit_rows_by_ids(table, column, old_values, columns, new_values):
    # 连接 MySQL 数据库
    conn = mysql.connector.connect(
        host='localhost',
        database='test',
        user='root',
        password='123456',
        auth_plugin='mysql_native_password'
    )
    cursor = conn.cursor()
    try:
        # 循环处理每一行新数据
        for i, old_value in enumerate(old_values):
            # 构建 SQL 更新语句
            update_query = f"UPDATE {table} SET "
            for col in columns:
                update_query += f"{col} = %s, "
            update_query = update_query[:-2]  # 去除最后一个逗号和空格
            update_query += f" WHERE {column} = %s"

            # 将新行的值添加到参数列表中
            params = new_values[i] + [old_value]

            # 执行更新操作
            cursor.execute(update_query, params)

        # 提交事务
        conn.commit()

        print(f"成功更新 {len(old_values)} 行.")

    except mysql.connector.Error as err:
        print(f"更新失败: {err}")

    finally:
        cursor.close()
        conn.close()



# 定义列名数组和新数据值二维数组
columns = ["序号", "八八", "拉拉"]
new_values = [["1", "啊啊啊啊", "顶顶顶顶"], ["2", "帆帆帆帆", "灌灌灌灌"]]
old_values = ["1", "2"]

# 调用函数更新数据
edit_rows_by_ids("try", "序号", old_values, columns, new_values)


