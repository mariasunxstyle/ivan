# Здесь будет логика управления: шаги, позиции, переходы, таймеры, кнопки

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Кнопки управления (во время шага, в разных строках)
control_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
control_keyboard.add(KeyboardButton("⏭️ Пропустить"))
control_keyboard.add(KeyboardButton("⛔ Завершить"))
control_keyboard.add(KeyboardButton("↩️ Назад на 2 шага"))
control_keyboard.add(KeyboardButton("📋 Вернуться к шагам"))

# Кнопки после завершения шага (в один ряд)
complete_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
complete_keyboard.add(
    KeyboardButton("▶️ Продолжить"),
    KeyboardButton("📋 Вернуться к шагам"),
    KeyboardButton("↩️ Назад на 2 шага"),
    KeyboardButton("⛔ Завершить")
)

# Меню шагов (без 0 ч)
steps_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
steps_keyboard.add(
    KeyboardButton("Шаг 1 (8 мин)"), KeyboardButton("Шаг 2 (9 мин)"),
    KeyboardButton("Шаг 3 (12 мин)"), KeyboardButton("Шаг 4 (20 мин)")
)
steps_keyboard.add(
    KeyboardButton("Шаг 5 (27 мин)"), KeyboardButton("Шаг 6 (38 мин)"),
    KeyboardButton("Шаг 7 (48 мин)"), KeyboardButton("Шаг 8 (1 ч 0 мин)")
)
steps_keyboard.add(
    KeyboardButton("Шаг 9 (1 ч 25 мин)"), KeyboardButton("Шаг 10 (1 ч 50 мин)"),
    KeyboardButton("Шаг 11 (2 ч 30 мин)"), KeyboardButton("Шаг 12 (3 ч 10 мин)")
)
steps_keyboard.add(KeyboardButton("ℹ️ Инфо"))

# Шаги и позиции с таймингом
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

# Форматирование времени
def format_duration(min_float):
    minutes = int(min_float)
    seconds = int((min_float - minutes) * 60)
    if seconds == 0:
        return f"{minutes} мин"
    else:
        return f"{minutes} мин {seconds} сек"

# Статусы
STEP_COMPLETED_MESSAGE = "Шаг завершён!"
ALL_STEPS_DONE_MESSAGE = "Ты завершил(а) все 12 шагов по методу суперкомпенсации!\nКожа адаптировалась, и теперь можно поддерживать загар в комфортном ритме ☀️"
SESSION_TERMINATED_MESSAGE = "Сеанс завершён.\nМожешь вернуться позже и начать заново ☀️"
BACK_LIMIT_MESSAGE = "Ты уже на самом начале. Назад на 2 шага нельзя."

# Приветствие
GREETING = """Привет, солнце! ☀️
Ты в таймере по методу суперкомпенсации.
Кожа адаптируется к солнцу постепенно — и загар становится ровным, глубоким и без ожогов.

Начинай с шага 1. Даже если уже немного загорел(а), важно пройти путь с начала.
Каждый новый день и после перерыва — возвращайся на 2 шага назад.

Хочешь разобраться подробнее — жми /info. Там всё по делу."""

# Инфо
INFO_TEXT = """ℹ️ Инфо
Метод суперкомпенсации — это безопасный, пошаговый подход к загару.
Он помогает коже адаптироваться к солнцу, снижая риск ожогов и пятен.

Рекомендуем загорать с 7:00 до 11:00 и после 17:00 — в это время солнце мягкое,
и при отсутствии противопоказаний можно загорать без SPF.

Так кожа включает свою естественную защиту: вырабатывается меланин и гормоны адаптации.

С 11:00 до 17:00 — солнце более агрессивное. Если остаёшься на улице —
надевай одежду, головной убор или используй SPF.

Каждый новый день и после перерыва — возвращайся на 2 шага назад.
Это нужно, чтобы кожа не перегружалась и постепенно усиливала защиту.

Если есть вопросы — пиши: @sunxbeach_director"""
