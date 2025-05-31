
event_counts = {
    "started": 0,
    "steps_started": 0,
    "sessions_ended": 0,
}

def log_event(event_type):
    if event_type in event_counts:
        event_counts[event_type] += 1

def get_event_stats():
    return (
        f"📊 Статистика:\n"
        f"— Нажали /start: {event_counts['started']}\n"
        f"— Начали шаг: {event_counts['steps_started']}\n"
        f"— Завершили сеанс: {event_counts['sessions_ended']}"
    )
