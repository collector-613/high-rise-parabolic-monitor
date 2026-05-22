import pymysql
import random
from datetime import datetime, timedelta

# 数据库配置
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "200606",
    "database": "parabolic_data",
    "charset": "utf8mb4"
}

def generate_parabolic_data():
    buildings = ["A栋", "B栋", "C栋", "D栋"]
    floors = list(range(3, 20))
    risk_levels = ["低风险", "中风险", "高风险"]
    base_time = datetime.now() - timedelta(days=7)

    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # 清空旧数据
    cursor.execute("TRUNCATE TABLE event")

    for i in range(100):
        building = random.choice(buildings)
        floor = random.choice(floors)
        # 关键：强制生成明显的坠落轨迹（起点高，落点低）
        x = random.randint(100, 500)
        y = random.randint(100, 500)
        speed = round(random.uniform(3, 25), 2)
        risk_level = "低风险" if speed < 10 else "中风险" if speed < 18 else "高风险"
        event_time = base_time + timedelta(seconds=random.randint(0, 7*24*3600))

        sql = """
            INSERT INTO event (building_id, floor, x, y, speed, risk_level, event_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (building, floor, x, y, speed, risk_level, event_time))

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ 100条带明显轨迹的数据已生成！")

if __name__ == "__main__":
    generate_parabolic_data()