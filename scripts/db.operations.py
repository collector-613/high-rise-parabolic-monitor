import mysql.connector

# 数据库连接配置（和之前一样）
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "200606",  # 你的MySQL密码
    "database": "parabolic_data"
}

def insert_event(building_id, floor, x, y, speed, risk_level):
    """
    把高空抛物事件数据写入数据库
    :param building_id: 楼栋号（比如"A栋"）
    :param floor: 楼层号
    :param x: 坐标x
    :param y: 坐标y
    :param speed: 物体速度
    :param risk_level: 风险等级（低/中/高）
    """
    conn = None
    cursor = None
    try:
        # 连接数据库
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # SQL语句
        sql = """
        INSERT INTO event (building_id, floor, x, y, speed, risk_level)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        # 执行插入
        cursor.execute(sql, (building_id, floor, x, y, speed, risk_level))
        conn.commit()
        print(f"✅ 事件数据写入成功！楼栋：{building_id}，楼层：{floor}")
        return True

    except Exception as e:
        print(f"❌ 写入失败：{e}")
        return False

    finally:
        # 关闭连接
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# 测试一下函数
if __name__ == "__main__":
    insert_event("B栋", 5, 600.0, 800.0, 10.2, "高风险")