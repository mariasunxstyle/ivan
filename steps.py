from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

POSITIONS = ["Лицом вверх", "На животе", "Левый бок", "Правый бок", "В тени"]

DURATIONS_MIN = [
    [1.5, 1.5, 1.0, 1.0, 3.0],
    [2.0, 2.0, 1.0, 1.0, 3.0],
    [3.0, 3.0, 1.5, 1.5, 5.0],
    [5.0, 5.0, 2.5, 2.5, 5.0],
    [7.0, 7.0, 3.0, 3.0, 7.0],
    [9.0, 9.0, 5.0, 5.0, 10.0],
    [12.0, 12.0, 7.0, 7.0, 10.0],
    [15.0, 15.0, 10.0, 10.0, 10.0],
    [20.0, 20.0, 15.0, 15.0, 15.0],
    [25.0, 25.0, 20.0, 20.0, 20.0],
    [35.0, 35.0, 25.0, 25.0, 30.0],
    [45.0, 45.0, 30.0, 30.0, 40.0],
]

def format_duration(mins):
    return f"{int(mins)} мин" if mins == int(mins) else f"{int(mins)} мин {int((mins - int(mins)) * 60)} сек"

# Шаги
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

# Управление во время шага — без "↩️ Назад"
def get_control_keyboard(step):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("⏭️ Пропустить"))
    kb.add(KeyboardButton("⛔ Завершить"))
    kb.add(KeyboardButton("📋 Вернуться к шагам"))
    return kb

# После завершения шага вручную — без "↩️ Назад"
def get_continue_keyboard(step):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("▶️ Продолжить"))
    kb.add(KeyboardButton("📋 Вернуться к шагам"))
    kb.add(KeyboardButton("⛔ Завершить"))
    return kb

# После завершения последнего шага
control_keyboard_full = ReplyKeyboardMarkup(resize_keyboard=True)
control_keyboard_full.add(KeyboardButton("📋 Вернуться к шагам"))
control_keyboard_full.add(KeyboardButton("↩️ Назад на 2 шага (после перерыва)"))
control_keyboard_full.add(KeyboardButton("⛔ Завершить"))

# После нажатия "Завершить"
end_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
end_keyboard.add(
    KeyboardButton("📋 Вернуться к шагам"),
    KeyboardButton("↩️ Назад на 2 шага (после перерыва)")
)
