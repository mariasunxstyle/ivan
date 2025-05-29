from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Клавиатура со всеми шагами
def steps_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    for i in range(12):
        minutes = sum(DURATIONS_MIN[i])
        label = f"{i+1} шаг ({int(minutes)} мин)" if minutes == int(minutes) else f"{i+1} шаг ({minutes:.1f} мин)"
        keyboard.insert(KeyboardButton(label))
    keyboard.add(KeyboardButton("ℹ️ Инфо"))
    return keyboard

# Кнопки управления во время шага
def get_control_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("⏭️ Пропустить"))
    keyboard.add(KeyboardButton("⛔ Завершить"))
    keyboard.add(KeyboardButton("↩️ Назад на 2 шага"))
    keyboard.add(KeyboardButton("📋 Вернуться к шагам"))
    return keyboard

# Кнопки после завершения шага
def get_continue_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        KeyboardButton("▶️ Продолжить"),
        KeyboardButton("📋 Вернуться к шагам"),
        KeyboardButton("↩️ Назад на 2 шага"),
        KeyboardButton("⛔ Завершить"),
    )
    return keyboard

# Полная клавиатура (если нужно явно)
control_keyboard_full = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton("⏭️ Пропустить")
).add(
    KeyboardButton("⛔ Завершить")
).add(
    KeyboardButton("↩️ Назад на 2 шага")
).add(
    KeyboardButton("📋 Вернуться к шагам")
)

# Просто клавиатура завершения
end_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton("📋 Вернуться к шагам"),
    KeyboardButton("↩️ Назад на 2 шага"),
)
