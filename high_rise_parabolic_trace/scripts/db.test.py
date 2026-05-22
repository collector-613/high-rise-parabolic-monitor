import mysql.connector

# 1. 连接数据库（把密码改成你自己的）
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="200606",  # ← 这里改成你自己的root密码
    database="parabolic_data"
)
cursor = conn.cursor()

# 2. 准备一条测试数据
test_data = {
    "building_id": "A栋",
    "floor": 3,
    "x": 520.5,
    "y": 780.2,
    "speed": 8.5,
    "risk_level": "中风险"
}

# 3. 写入数据库
sql = """
INSERT INTO event (building_id, floor, x, y, speed, risk_level)
VALUES (%s, %s, %s, %s, %s, %s)
"""
cursor.execute(sql, (
    test_data["building_id"],
    test_data["floor"],
    test_data["x"],
    test_data["y"],
    test_data["speed"],
    test_data["risk_level"]
))
conn.commit()
print("✅ 测试数据写入成功！")

# 4. 关闭连接
cursor.close()
conn.close()