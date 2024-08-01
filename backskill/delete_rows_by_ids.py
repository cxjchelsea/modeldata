# _*_ coding: utf-8 _*_
# @File:    delete_rows_by_ids
# @Time:    2024/4/16 9:14
# @Author:  chenxuejiao
# @Contact: 15801102378@163.com
# @Version: V 0.1

def delete_rows_by_ids(ids,table):
    # 建立数据库连接
    conn = connect_to_database()

    try:
        # 创建游标对象
        cursor = conn.cursor()

        # 构建 SQL 删除语句，并使用参数占位符来传递表名和 id 数组
        sql = f"DELETE FROM {table} WHERE 序号 IN ({', '.join(['%s'] * len(ids))})"

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