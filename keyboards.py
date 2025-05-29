from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_control_keyboard(step):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("⏭️ Пропустить"))
    kb.add(KeyboardButton("⛔ Завершить"))
    if step <= 2:
        kb.add(KeyboardButton("↩️ Назад на шаг 1 (если был перерыв)"))
    else:
        kb.add(KeyboardButton("↩️ Назад на 2 шага (после перерыва)"))
    kb.add(KeyboardButton("📋 Вернуться к шагам"))
    return kb
