
from datetime import datetime
from state import user_data

def track_user(msg):
    user = msg.from_user
    user_data[user.id] = {
        "username": user.username,
        "name": user.full_name,
        "last_active": datetime.now()
    }

def get_stats_message():
    total = len(user_data)
    today = datetime.now().date()
    today_users = [v for v in user_data.values() if v["last_active"].date() == today]
    recent = sorted(user_data.items(), key=lambda x: x[1]["last_active"], reverse=True)[:5]
    recent_list = "\n".join([f"— @{v['username'] or v['name']}" for _, v in recent])
    return f"👥 Всего пользователей: {total}\n📆 Сегодня заходили: {len(today_users)}\n\nПоследние активные:\n{recent_list}"
