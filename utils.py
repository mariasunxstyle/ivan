# utils.py

from aiogram import types

GREETING = "Привет, солнце! ☀️\nТы в таймере по методу суперкомпенсации.\nКожа адаптируется к солнцу постепенно — и загар становится ровным, глубоким и без ожогов."

INFO_TEXT = "Метод суперкомпенсации — это безопасный, пошаговый подход к загару.\nОн помогает коже адаптироваться к солнцу, снижая риск ожогов и пятен.\nРекомендуем загорать с 7:00 до 11:00 и после 17:00.\nС 11:00 до 17:00 — солнце агрессивное, используй одежду или SPF."

STEP_COMPLETED_MESSAGE = "Шаг завершён! Хочешь продолжить?"

SESSION_TERMINATED_MESSAGE = "Сеанс завершён. Можешь вернуться позже и начать заново ☀️"

BACK_LIMIT_MESSAGE = "Ты и так в самом начале. Назад уже некуда ☀️"

def format_duration(minutes):
    m = int(minutes)
    s = int(round((minutes - m) * 60))
    if m == 0:
        return f"{s} сек"
    elif s == 0:
        return f"{m} мин"
    else:
        return f"{m} мин {s} сек"

# Кнопки шагов
steps_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
for i, durations in enumerate([
    sum(d) for d in [
        [1.5, 1.5, 1.0, 1.0, 3.0],
        [2.0, 2.0, 1.0, 1.0, 3.0],
        [3.0, 3.0, 1.5, 1.5, 5.0],
        [5.0, 5.0, 2.5, 2.5, 5.0],
        [7.0, 7.0, 3.0, 3.0, 7.0],
        [9.0, 9.0, 5.0, 5.0, 10.0],
        [12.0, 12.0, 7.0, 7.0, 10.0],
        [15.0, 15.0, 10.0, 10.0, 10.0],
        [20.0, 20.0, 15.0, 15.0, 15.0],
        [25.0, 25.0, 20.0, 20.0, 20.0],
        [35.0, 35.0, 25.0, 25.0, 30.0],
        [45.0, 45.0, 30.0, 30.0, 40.0],
    ]
]):
    m = int(durations)
    h = m // 60
    m = m % 60
    label = f"{h} ч {m} мин" if h else f"{m} мин"
    steps_keyboard.insert(types.KeyboardButton(f"Шаг {i+1} ({label})"))

steps_keyboard.add(types.KeyboardButton("ℹ️ Инфо"))

# Кнопки управления
control_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
control_keyboard.add(
    types.KeyboardButton("⏭️ Пропустить"),
    types.KeyboardButton("⛔ Завершить"),
    types.KeyboardButton("↩️ Назад на 2 шага"),
    types.KeyboardButton("📋 Вернуться к шагам"),
)

control_keyboard_full_vertical = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
control_keyboard_full_vertical.add(
    types.KeyboardButton("▶️ Продолжить"),
    types.KeyboardButton("📋 Вернуться к шагам"),
    types.KeyboardButton("↩️ Назад на 2 шага"),
    types.KeyboardButton("⛔ Завершить"),
)
