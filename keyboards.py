
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from steps import steps

def get_step_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    for step in steps:
        total = sum([t for _, t in step["positions"]])
        h, m = divmod(total, 60)
        label = f"Шаг {step['step']} — {h} ч {m} мин" if h else f"Шаг {step['step']} — {m} мин"
        keyboard.insert(KeyboardButton(label))
    keyboard.add(KeyboardButton("ℹ️ Инфо"))
    return keyboard

def get_control_keyboard():
    return ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton("⏭️ Пропустить"),
        KeyboardButton("⛔ Завершить"),
        KeyboardButton("↩️ Назад на 2 шага (если был перерыв)"),
        KeyboardButton("📋 Вернуться к шагам")
    )
