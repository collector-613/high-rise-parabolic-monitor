import warnings
warnings.filterwarnings("ignore")
import pymysql
import pandas as pd
import json
import matplotlib.pyplot as plt
import os

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 数据库配置（和你原来的一样）
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "200606",
    "database": "parabolic_data",
    "charset": "utf8mb4"
}


def analyze_event(df):
    """分析高空抛物事件数据"""
    print("\n--- 事件数据统计分析 ---")
    print(f"✅ 共读取到 {len(df)} 条抛物事件记录")
    print(f"✅ 建筑编号：{df['building_id'].unique()}")
    print(f"✅ 楼层分布：{df['floor'].value_counts().to_dict()}")
    print(f"✅ 风险等级分布：{df['risk_level'].value_counts().to_dict()}")
    print(f"✅ 平均速度：{df['speed'].mean():.2f} m/s")
    print(f"✅ 最高速度：{df['speed'].max():.2f} m/s")


def plot_trajectory(df):
    """绘制抛物轨迹图，保存到data文件夹"""
    print("\n--- 开始绘制轨迹图 ---")
    plt.figure(figsize=(10, 6))

    plt.plot(df['x'], df['y'], marker='o', color='red', linestyle='-', label="抛物轨迹")
    plt.scatter(df['x'].iloc[0], df['y'].iloc[0], color='green', s=100, label="起点")
    plt.scatter(df['x'].iloc[-1], df['y'].iloc[-1], color='blue', s=100, label="落点")

    plt.title("高空抛物运动轨迹")
    plt.xlabel("水平坐标 X")
    plt.ylabel("垂直坐标 Y")
    plt.legend()
    plt.grid(True)

    # 保存到data文件夹
    data_path = os.path.join(os.path.dirname(__file__), "../data/trace_plot.png")
    plt.savefig(data_path)
    print("✅ 轨迹图已保存到 data/trace_plot.png")
    plt.close()


def main():
    try:
        conn = pymysql.connect(**DB_CONFIG)
        print("✅ 数据库连接成功")

        sql = "SELECT * FROM event"
        df = pd.read_sql(sql, conn)
        print(f"✅ 一共读取到 {len(df)} 条记录")

        # 保存数据到data文件夹
        json_path = os.path.join(os.path.dirname(__file__), "../data/event_data.json")
        df.to_json(json_path, orient="records", force_ascii=False, indent=2)
        print("✅ 数据已保存到 data/event_data.json")

        analyze_event(df)
        plot_trajectory(df)

        conn.close()
        print("\n🎉 数据分析完成！")

    except Exception as e:
        print(f"❌ 运行报错：{e}")
        return None


if __name__ == "__main__":
    main()