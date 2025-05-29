
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_control_keyboard(step):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(KeyboardButton("⏭️ Пропустить"))
    kb.row(KeyboardButton("⛔ Завершить"))
    if step <= 2:
        kb.row(KeyboardButton("↩️ Вернуться на шаг 1"))
    else:
        kb.row(KeyboardButton("↩️ Назад на 2 шага (после перерыва)"))
    kb.row(KeyboardButton("📋 Вернуться к шагам"))
    return kb
