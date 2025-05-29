from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Клавиатура с шагами (3 ряда по 4 шага)
step_buttons = [
    [KeyboardButton("Шаг 1"), KeyboardButton("Шаг 2"), KeyboardButton("Шаг 3"), KeyboardButton("Шаг 4")],
    [KeyboardButton("Шаг 5"), KeyboardButton("Шаг 6"), KeyboardButton("Шаг 7"), KeyboardButton("Шаг 8")],
    [KeyboardButton("Шаг 9"), KeyboardButton("Шаг 10"), KeyboardButton("Шаг 11"), KeyboardButton("Шаг 12")],
    [KeyboardButton("ℹ️ Инфо")]
]
steps_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=step_buttons)

# Кнопки управления во время выполнения шага
def get_control_keyboard(step: int):
    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton("⏭️ Пропустить")],
        [KeyboardButton("⛔ Завершить")],
        [KeyboardButton(get_back_button_label(step))],
        [KeyboardButton("📋 Вернуться к шагам")]
    ])

# Кнопки после завершения шага
def get_continue_keyboard(step: int):
    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[
        KeyboardButton("▶️ Продолжить"),
        KeyboardButton("📋 Вернуться к шагам"),
        KeyboardButton(get_back_button_label(step)),
        KeyboardButton("⛔ Завершить")
    ]])

# Кнопки после завершения сеанса
end_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[
    KeyboardButton("📋 Вернуться к шагам"),
    KeyboardButton("↩️ Назад (если был перерыв)")
]])

# Название кнопки "назад" для шагов 1–2
def get_back_button_label(step: int) -> str:
    if step <= 2:
        return "↩️ Вернуться к шагу 1"
    return "↩️ Назад на 2 шага"
