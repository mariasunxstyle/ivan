# utils.py

from aiogram import types

# Сообщения
GREETING = (
    "Привет, солнце! ☀️\n"
    "Ты в таймере по методу суперкомпенсации.\n"
    "Кожа адаптируется к солнцу постепенно — и загар получается ровным, глубоким и без ожогов.\n\n"
    "Метод основан на научных принципах: короткие интервалы активируют выработку меланина и гормонов адаптации.\n"
    "Такой подход снижает риск ожогов и делает загар устойчивым.\n\n"
    "Начинай с шага 1 — даже если уже немного загорел(а).\n"
    "Каждый новый день и после перерыва — возвращайся на 2 шага назад.\n\n"
    "Хочешь подробности — жми /info."
)

INFO_TEXT = (
    "ℹ️ Инфо\n"
    "Метод суперкомпенсации — научно обоснованный способ безопасного загара.\n"
    "Ты проходишь 12 шагов — каждый с таймингом и сменой позиций.\n\n"
    "Как использовать:\n"
    "1. Начни с шага 1\n"
    "2. Включи таймер и следуй позициям\n"
    "3. Каждый новый день и после любого перерыва — возвращайся на 2 шага назад\n"
    "4. После завершения всех 12 шагов — можешь поддерживать загар в комфортном ритме\n\n"
    "Рекомендуем загорать с 7:00 до 11:00 и после 17:00 — в это время солнце мягкое, и при отсутствии противопоказаний можно загорать без SPF.\n"
    "С 11:00 до 17:00 — солнце более агрессивное. Если остаёшься на улице — надевай одежду или используй SPF.\n\n"
    "Если есть вопросы — пиши: @sunxbeach_director"
)

STEP_COMPLETED_MESSAGE = "Шаг завершён!"
SESSION_TERMINATED_MESSAGE = "Сеанс завершён.\nМожешь вернуться позже и начать заново ☀️"

# Позиции
POSITIONS = ["Лицом вверх", "На животе", "Левый бок", "Правый бок", "В тени"]

# Длительности (в минутах)
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

# Формат времени
def format_duration(minutes):
    m = int(minutes)
    s = int((minutes - m) * 60)
    if s == 0:
        return f"{m} мин"
    elif m == 0:
        return f"{s} сек"
    else:
        return f"{m} мин {s} сек"

# Клавиатура шагов (ч мин)
steps_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
for i, durations in enumerate(DURATIONS_MIN):
    total = int(sum(durations))
    h = total // 60
    m = total % 60
    label = f"{h} ч {m} мин" if h else f"{m} мин"
    steps_keyboard.insert(types.KeyboardButton(f"Шаг {i+1} ({label})"))
steps_keyboard.add(types.KeyboardButton("ℹ️ Инфо"))

# Клавиатура во время выполнения позиции
control_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
control_keyboard.add(types.KeyboardButton("⏭️ Пропустить"))
control_keyboard.add(types.KeyboardButton("⛔ Завершить"))
control_keyboard.add(types.KeyboardButton("↩️ Назад на 2 шага"))
control_keyboard.add(types.KeyboardButton("📋 Вернуться к шагам"))

# Клавиатура после завершения позиции (4 кнопки в 4 строки)
complete_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
complete_keyboard.add(types.KeyboardButton("▶️ Продолжить"))
complete_keyboard.add(types.KeyboardButton("📋 Вернуться к шагам"))
complete_keyboard.add(types.KeyboardButton("↩️ Назад на 2 шага"))
complete_keyboard.add(types.KeyboardButton("⛔ Завершить"))

# Клавиатура после завершения сеанса или 12 шага (только 2 кнопки)
control_keyboard_end = types.ReplyKeyboardMarkup(resize_keyboard=True)
control_keyboard_end.add(types.KeyboardButton("↩️ Назад на 2 шага"))
control_keyboard_end.add(types.KeyboardButton("📋 Вернуться к шагам"))
