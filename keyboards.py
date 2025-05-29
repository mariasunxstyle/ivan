from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from steps import DURATIONS_MIN

steps_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
step_buttons = []
for i, row in enumerate(DURATIONS_MIN):
    total = sum(row)
    h = int(total // 60)
    m = int(total % 60)
    label = f"Шаг {i + 1} ({f'{h} ч ' if h else ''}{m} мин)"
    step_buttons.append(KeyboardButton(label))
for i in range(0, len(step_buttons), 4):
    steps_keyboard.add(*step_buttons[i:i + 4])
steps_keyboard.add(KeyboardButton("ℹ️ Инфо"))

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

def get_continue_keyboard(step):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("▶️ Продолжить"))
    kb.add(KeyboardButton("📋 Вернуться к шагам"))
    if step <= 2:
        kb.add(KeyboardButton("↩️ Назад на шаг 1 (если был перерыв)"))
    else:
        kb.add(KeyboardButton("↩️ Назад на 2 шага (после перерыва)"))
    kb.add(KeyboardButton("⛔ Завершить"))
    return kb

control_keyboard_full = ReplyKeyboardMarkup(resize_keyboard=True)
control_keyboard_full.add(KeyboardButton("📋 Вернуться к шагам"))
control_keyboard_full.add(KeyboardButton("↩️ Назад на 2 шага (после перерыва)"))
control_keyboard_full.add(KeyboardButton("⛔ Завершить"))

end_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
end_keyboard.add(
    KeyboardButton("📋 Вернуться к шагам"),
    KeyboardButton("↩️ Назад на 2 шага (после перерыва)")
)
