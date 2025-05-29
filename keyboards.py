from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def steps_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    for i, minutes in enumerate([
        "8 мин", "9 мин", "14 мин", "20 мин",
        "27 мин", "38 мин", "49 мин", "56 мин",
        "64 мин", "70 мин", "80 мин", "150 мин"
    ], start=1):
        kb.insert(KeyboardButton(f"Шаг {i} — {minutes}"))
    kb.add(KeyboardButton("ℹ️ Инфо"))
    return kb

def get_control_keyboard(step):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    if step == 1:
        kb.add(KeyboardButton("↩️ Назад на шаг 1 (если был перерыв)"))
    elif step <= 2:
        kb.add(KeyboardButton("↩️ Назад на шаг 1 (если был перерыв)"))
    else:
        kb.add(KeyboardButton("↩️ Назад на 2 шага (после перерыва)"))
    kb.add(KeyboardButton("⏭️ Пропустить"))
    kb.add(KeyboardButton("📋 Вернуться к шагам"))
    kb.add(KeyboardButton("⛔ Завершить"))
    return kb

def get_continue_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(
        KeyboardButton("▶️ Продолжить"),
        KeyboardButton("📋 Вернуться к шагам"),
        KeyboardButton("↩️ Назад на 2 шага (если был перерыв)"),
        KeyboardButton("⛔ Завершить")
    )
    return kb

def control_keyboard_full():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("⏭️ Пропустить"))
    kb.add(KeyboardButton("📋 Вернуться к шагам"))
    kb.add(KeyboardButton("↩️ Назад на 2 шага (если был перерыв)"))
    kb.add(KeyboardButton("⛔ Завершить"))
    return kb

def end_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(
        KeyboardButton("📋 Вернуться к шагам"),
        KeyboardButton("↩️ Назад на 2 шага (если был перерыв)")
    )
    return kb

