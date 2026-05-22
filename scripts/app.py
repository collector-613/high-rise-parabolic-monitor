from flask import Flask, render_template
import json
import os
import pandas as pd
import webbrowser
import threading
from datetime import datetime, timedelta
import numpy as np

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)


def convert_numpy_types(obj):
    """递归把 numpy 类型转为普通 Python 类型"""
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return obj


@app.route("/")
def index():
    json_path = os.path.join(os.path.dirname(__file__), "../data/event_data.json")
    df = pd.read_json(json_path)

    avg_speed = round(float(df['speed'].mean()), 2)
    max_speed = round(float(df['speed'].max()), 2)

    risk_counts = df['risk_level'].value_counts().to_dict()
    risk_counts.setdefault('低风险', 0)
    risk_counts.setdefault('中风险', 0)
    risk_counts.setdefault('高风险', 0)

    floor_counts = df['floor'].value_counts().to_dict()
    build_counts = df['building_id'].value_counts().to_dict()
    buildings = list(build_counts.keys())

    df['hour'] = pd.to_datetime(df['event_time']).dt.hour
    time_dist = [
        len(df[(df['hour'] >= 0) & (df['hour'] < 6)]),
        len(df[(df['hour'] >= 6) & (df['hour'] < 12)]),
        len(df[(df['hour'] >= 12) & (df['hour'] < 18)]),
        len(df[(df['hour'] >= 18) & (df['hour'] < 24)])
    ]

    # 轨迹数据（关键修复：强制转为普通int）
    trajectories = []
    for i in range(min(4, len(df))):
        row = df.iloc[i]
        x = int(row['x'])
        y = int(row['y'])
        trajectories.append([
            [x - 100, y + 100],
            [x, y]
        ])

    # 近7天抛物趋势数据
    today = datetime.now()
    week_days = []
    week_counts = []
    for i in range(7):
        day = today - timedelta(days=6 - i)
        week_days.append(day.strftime('%m-%d'))
        next_day = day + timedelta(days=1)
        cnt = len(df[(pd.to_datetime(df['event_time']) >= day) & (pd.to_datetime(df['event_time']) < next_day)])
        week_counts.append(cnt)

    # 实时事件列表（取最新10条）
    events = df.sort_values('event_time', ascending=False).head(10).to_dict('records')

    data = {
        "avg_speed": avg_speed,
        "max_speed": max_speed,
        "risk_counts": risk_counts,
        "floor_counts": floor_counts,
        "build_counts": build_counts,
        "buildings": buildings,
        "time_dist": time_dist,
        "trajectories": trajectories,
        "week_days": week_days,
        "week_counts": week_counts,
        "events": events
    }

    # 关键：递归转换所有 numpy 类型，避免 JSON 报错
    data = {k: convert_numpy_types(v) for k, v in data.items()}

    return render_template("index.html", data=data)


def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")


if __name__ == "__main__":
    threading.Timer(1, open_browser).start()
    print("✅ 高空抛物监测大屏已启动，访问地址：http://127.0.0.1:5000")
    app.run(debug=True, use_reloader=False)