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
#
# def modify_table_headers(table, new_column_names):
#     try:
#         # 连接到 MySQL 数据库
#         conn = connect_to_database()
#
#         # 创建游标
#         cursor = conn.cursor()
#
#         # 获取当前表的列名
#         cursor.execute(f"SHOW COLUMNS FROM {table}")
#         current_columns_info = cursor.fetchall()
#
#         # 提取当前列名及其其他信息
#         current_column_names = [column[0] for column in current_columns_info]
#
#         # 检查输入数组和当前列名的长度是否一致
#         if len(new_column_names) != len(current_column_names):
#             print("输入数组和当前列名的长度不一致。")
#             return
#
#         # 构建修改列名的语句
#         for i, (old_column_name, new_column_name) in enumerate(zip(current_column_names, new_column_names)):
#             if old_column_name != new_column_name:
#                 alter_query = f"ALTER TABLE {table} CHANGE COLUMN {old_column_name} {new_column_name} {current_columns_info[i][1]}"
#                 cursor.execute(alter_query)
#
#         # 提交事务
#         conn.commit()
#
#         print("表头修改成功。")
#
#     except mysql.connector.Error as err:
#         print("Error:", err)
#
#     finally:
#         # 关闭游标和连接
#         if 'cursor' in locals():
#             cursor.close()
#         if 'conn' in locals():
#             conn.close()

def modify_table_headers(table, new_column_names):
    try:
        # 连接到 MySQL 数据库
        conn = connect_to_database()

        # 创建游标
        cursor = conn.cursor()

        # 获取当前表的列名和数据类型信息
        cursor.execute(f"SHOW COLUMNS FROM {table}")
        current_columns_info = cursor.fetchall()

        # 从列信息中提取列名和数据类型
        current_column_names = [column[0] for column in current_columns_info]

        # 检查输入数组和当前列名的长度是否一致
        if len(new_column_names) != len(current_column_names):
            print("输入数组和当前列名的长度不一致。")
            return

        # 查找并保留序号列
        index_column = None
        for i, column_info in enumerate(current_columns_info):
            if column_info[0] == '序号':
                index_column = current_column_names.pop(i)
                current_columns_info.pop(i)
                break

        # 构建修改列名的语句
        for i, (old_column_name, new_column_name) in enumerate(zip(current_column_names, new_column_names)):
            if old_column_name != new_column_name:
                alter_query = f"ALTER TABLE {table} CHANGE COLUMN {old_column_name} {new_column_name} {current_columns_info[i][1]}"
                cursor.execute(alter_query)

        # 添加序号列回表中
        if index_column:
            cursor.execute(f"ALTER TABLE {table} ADD COLUMN {index_column} INT FIRST")

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

# 示例用法
table = 'information_roll_line'
new_column_names = ['ID', '产线名称', '工厂设计', '投产时间', '设计产能万吨', '最大板坯厚度mm', '最小板坯厚度mm', '板坯最大宽度mm', '板坯最小宽度mm', ' 板坯最大长度m', ' 板坯最小长度m', '最大板坯重量吨', '设计成品最大厚度mm', '设计成品最小厚度mm', '已批量生产最小成品厚度mm', '已批量生产最大成品厚度mm', '设计成品最大宽度mm', '设计成品最小宽度mm', '已批量生产最小成品宽度mm', '已批量生产最大成品宽度mm', '热装热送率', '板坯库管理系统有无', '板坯库管理系统供货商', '板坯号自动识别', '板坯号自动识别装置供货商', '加热炉前辊道测宽仪台', '加热炉前测宽仪供货商', '加热炉座', '加热炉设备供货商', '加热炉自动化原供货商', '加热炉原设计是否有二级', '加热炉自动化改造商', '加热炉改造后是否有二级', '粗轧机前测宽仪台', '粗轧机前测宽仪供货商', '是否有定宽压力机', '锤头工作方式步进连续', '定宽机最大侧压量mm', '定宽机电机功率KW', '定宽机最大轧制力Ton', 'E1立辊压头', 'R1平辊压头', 'E1至R1中心线之间的距离m', 'R1粗轧平辊轧辊数个', 'R1最大轧制力Ton', 'R1最大轧制速度ms', 'R1粗轧主电机功率KW', 'R1粗轧主电机型号', 'R1粗轧主电机类型', 'R1粗轧主电机控制方式', 'R1至E2中心线之间的距离m', 'E2立辊压头', 'R2平辊压头', 'E2至R2中心线之间的距离m', 'R2粗轧平辊轧辊数个', 'R2最大轧制力Ton', 'R2粗轧主电机功率KW', 'R2粗轧主电机型号', 'R2粗轧主电机类型', 'R2粗轧主电机控制方式', '粗轧机组后测宽仪台', '粗轧机组后测宽仪供货商', '粗轧设备供货商', '粗轧镰刀弯检测装置台', '粗轧镰刀弯检测装置是否用于在线闭环控制', '粗轧镰刀弯检测装置供货商', '粗轧电气原供货商', '粗轧主电机供货商', '粗轧主传动是否已改造', '粗轧主传动改造供货商', '粗轧自动化供货商', '粗轧自动化是否有二级', '热卷箱台', '热卷箱设备供货商', '热卷箱自动化供货商', '精轧机组架', '精轧机组设备供货商', '精轧机组电气原供货商', '精轧主电机类型', '精轧主电机控制方式', 'F1主电机功率KW', 'F2主电机功率KW', 'F3主电机功率KW', 'F4主电机功率KW', 'F5主电机功率KW', 'F6主电机功率KW', 'F7主电机功率KW', 'F8主电机功率KW', 'F1最大轧制力Ton', 'F2最大轧制力Ton', 'F3最大轧制力Ton', 'F4最大轧制力Ton', 'F5最大轧制力Ton', 'F6最大轧制力Ton', 'F7最大轧制力Ton', 'F8最大轧制力Ton', 'F1最大弯辊力Ton', 'F2最大弯辊力Ton', 'F3最大弯辊力Ton', 'F4最大弯辊力Ton', 'F5最大弯辊力Ton', 'F6最大弯辊力Ton', 'F7最大弯辊力Ton', 'F8最大弯辊力Ton', 'F1最大窜辊量mm', 'F2最大窜辊量mm', 'F3最大窜辊量mm', 'F4最大窜辊量mm', 'F5最大窜辊量mm', 'F6最大窜辊量mm', 'F7最大窜辊量mm', 'F8最大窜辊量mm', 'F1工作辊最大直径mm', 'F2工作辊最大直径mm', 'F3工作辊最大直径mm', 'F4工作辊最大直径mm', 'F5工作辊最大直径mm', 'F6工作辊最大直径mm', 'F7工作辊最大直径mm', 'F8工作辊最大直径mm', 'F1工作辊最小直径mm', 'F2工作辊最小直径mm', 'F3工作辊最小直径mm', 'F4工作辊最小直径mm', 'F5工作辊最小直径mm', 'F6工作辊最小直径mm', 'F7工作辊最小直径mm', 'F8工作辊最小直径mm', 'F1支撑辊最大直径mm', 'F2支撑辊最大直径mm', 'F3支撑辊最大直径mm', 'F4支撑辊最大直径mm', 'F5支撑辊最大直径mm', 'F6支撑辊最大直径mm', 'F7支撑辊最大直径mm', 'F8支撑辊最大直径mm', 'F1支撑辊最小直径mm', 'F2支撑辊最小直径mm', 'F3支撑辊最小直径mm', 'F4支撑辊最小直径mm', 'F5支撑辊最小直径mm', 'F6支撑辊最小直径mm', 'F7支撑辊最小直径mm', 'F8支撑辊最小直径mm', 'F1最大转速rpm', 'F2最大转速rpm', 'F3最大转速rpm', 'F4最大转速rpm', 'F5最大转速rpm', 'F6最大转速rpm', 'F7最大转速rpm', 'F8最大转速rpm', 'F1额定转速rpm', 'F2额定转速rpm', 'F3额定转速rpm', 'F4额定转速rpm', 'F5额定转速rpm', 'F6额定转速rpm', 'F7额定转速rpm', 'F8额定转速rpm', 'F1减速箱传动比', 'F2减速箱传动比', 'F3减速箱传动比', 'F4减速箱传动比', 'F5减速箱传动比', 'F6减速箱传动比', 'F7减速箱传动比', 'F8减速箱传动比', '精轧机组各机架中心线之间的距离m', '末架最大轧制速度ms', '精轧机组自动化供货商', '精轧机组自动化是否有二级', '板形二级是否投用', '磨辊间管理系统有无', '磨辊间管理系统供货商', 'MES系统有无', 'MES系统供货商', '精轧机后测宽仪台', '精轧机后测宽仪供货商', '精轧机后测厚仪台', '精轧机后测厚仪供货商', '精轧机后多功能仪台', '精轧机后多功能仪供货商', '精轧机后单配平直度仪台', '精轧机后平直度仪供货商', '精轧跑偏在线检测装置台', '精轧跑偏在线检测装置是否用于在线控制', '精轧跑偏在线检测装置供货商', '是否有超快速冷却', '超快冷组数', '层冷粗调集管组', '层冷精调集管组', '表面质量检测装置台', '表面质量检测装置供货商', '地下卷取机台', 'col_1号地下卷取机功率KW', 'col_2号地下卷取机功率KW', 'col_3号地下卷取机功率KW', '地下卷取机最大卷径mm', '地下卷取机内径mm', '地下卷取机最大速度 ms', '地下卷取机最大张力 KN', '自动钢卷喷号有无', '自动钢卷喷号装置供货商', '成品库管理系统有无', '成品库管理系统供货商', '是否实现集控操作室合并为1个', '集控供货商']

modify_table_headers(table, new_column_names)
