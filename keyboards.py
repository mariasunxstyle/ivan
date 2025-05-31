from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

steps_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
for i in range(1, 3):
    steps_keyboard.add(KeyboardButton(f"Шаг {i}"))

def get_control_keyboard(step):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("⏭️ Пропустить"))
    markup.add(KeyboardButton("⛔ Завершить"))

    if step in [1, 2]:
        markup.add(KeyboardButton("↩️ Назад на шаг 1 (если был перерыв)"))
    else:
        markup.add(KeyboardButton("↩️ Назад на 2 шага (если был перерыв)"))

    markup.add(KeyboardButton("📋 Вернуться к шагам"))
    return markup
