
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Клавиатура шагов с указанием времени
step_durations = [
    [8, 9, 10, 11, 13], [11, 12, 14, 15, 18], [13, 14, 16, 17, 20],
    [15, 16, 18, 19, 22], [17, 18, 20, 21, 24], [19, 20, 22, 23, 26],
    [21, 22, 24, 25, 28], [23, 24, 26, 27, 30], [25, 26, 28, 29, 32],
    [27, 28, 30, 31, 34], [29, 30, 32, 33, 36], [31, 32, 34, 35, 38]
]

def format_duration(step_index):
    total = sum(step_durations[step_index])
    hours = total // 60
    minutes = total % 60
    if hours:
        return f"{hours} ч {minutes} мин" if minutes else f"{hours} ч"
    return f"{minutes} мин"

# Клавиатура с 12 шагами
buttons = [
    KeyboardButton(f"Шаг {i+1} ({format_duration(i)})")
    for i in range(12)
]
steps_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(*buttons[:4]).add(*buttons[4:8]).add(*buttons[8:])

# Управляющие кнопки
def get_control_keyboard():
    return ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton("⏭️ Пропустить")
    ).add(
        KeyboardButton("⛔ Завершить")
    ).add(
        KeyboardButton("↩️ Назад на 2 шага (если был перерыв)")
    ).add(
        KeyboardButton("📋 Вернуться к шагам")
    )

def get_continue_keyboard():
    return ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton("▶️ Продолжить"),
        KeyboardButton("📋 Вернуться к шагам"),
        KeyboardButton("↩️ Назад на 2 шага (если был перерыв)"),
        KeyboardButton("⛔ Завершить")
    )
