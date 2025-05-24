
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from steps import steps

def human_time(m):
    h, mm = divmod(int(m), 60)
    return f"{h} ч {mm} мин" if h else f"{mm} мин"

def get_step_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    for s, mins in steps:
        kb.insert(KeyboardButton(f"Шаг {s} ({human_time(mins)})"))
    kb.add(KeyboardButton("ℹ️ Инфо"))
    return kb

def get_control_keyboard():
    return ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton("⏭️ Пропустить"),
        KeyboardButton("⛔ Завершить"),
        KeyboardButton("↩️ Назад на 2 шага"),
        KeyboardButton("📋 Вернуться к шагам")
    )

def get_post_step_keyboard():
    return ReplyKeyboardMarkup(resize_keyboard=True).add(
        [KeyboardButton("⏭️ Продолжить")],
        [KeyboardButton("📋 Вернуться к шагам")],
        [KeyboardButton("↩️ Назад на 2 шага")],
        [KeyboardButton("⛔ Завершить")]
    )
