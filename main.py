# main.py на основе рабочей схемы без FSM
import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

API_TOKEN = os.getenv("TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL") or "@sunxstyle"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# ======= ДАННЫЕ =======
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

# Кнопки
control_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
control_keyboard.add(types.KeyboardButton("⏭️ Пропустить"))
control_keyboard.add(types.KeyboardButton("⛔ Завершить"))
control_keyboard.add(types.KeyboardButton("↩️ Назад на 2 шага (после перерыва)"))
control_keyboard.add(types.KeyboardButton("📋 Вернуться к шагам"))

control_keyboard_full = ReplyKeyboardMarkup(resize_keyboard=True)
control_keyboard_full.add(types.KeyboardButton("📋 Вернуться к шагам"))
control_keyboard_full.add(types.KeyboardButton("↩️ Назад на 2 шага (после перерыва)"))
control_keyboard_full.add(types.KeyboardButton("⛔ Завершить"))

end_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
end_keyboard.add(
    types.KeyboardButton("📋 Вернуться к шагам"),
    types.KeyboardButton("↩️ Назад на 2 шага (после перерыва)")
)

steps_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
for i, row in enumerate(DURATIONS_MIN):
    min_total = int(sum(row))
    h = min_total // 60
    m = min_total % 60
    label = f"Шаг {i+1} ({f'{h} ч ' if h else ''}{m} мин)"
    steps_keyboard.add(types.KeyboardButton(label))
steps_keyboard.add(types.KeyboardButton("ℹ️ Инфо"))

# Сообщения
GREETING = """Привет, солнце! ☀️
Ты в таймере по методу суперкомпенсации.
Кожа адаптируется к солнцу постепенно — и загар получается ровный, глубокий и без ожогов.

Метод помогает загорать быстрее, глубже и без ожогов.

Начинай с шага 1. Даже если уже немного загорел(а), важно пройти путь с начала.
Каждый новый день и после перерыва — возвращайся на 2 шага назад.

Хочешь разобраться подробнее — жми /info. Там всё по делу."""

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

STEP_COMPLETED = "Ты прошёл(ла) 12 шагов по методу суперкомпенсации ☀️\nКожа адаптировалась. Теперь можно поддерживать загар в своём ритме."
SESSION_DONE = "Сеанс завершён. Можешь вернуться позже и начать заново ☀️"
BACK_LIMIT = None

# СОСТОЯНИЕ
user_state = {}
tasks = {}

# ХЭНДЛЕРЫ
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer(GREETING, reply_markup=steps_keyboard)

@dp.message_handler(commands=['info'])
@dp.message_handler(lambda m: m.text == "ℹ️ Инфо")
async def send_info(message: types.Message):
    await message.answer(INFO_TEXT)

@dp.message_handler(lambda m: m.text.startswith("Шаг "))
async def handle_step(message: types.Message):
    user_id = message.chat.id
    step_num = int(message.text.split()[1])
    user_state[user_id] = {"step": step_num, "position": 0}
    await start_position(user_id)

async def start_position(user_id):
    state = user_state.get(user_id)
    if not state:
        return
    step = state["step"]
    pos = state["position"]
    if step > 12:
        await bot.send_message(user_id, STEP_COMPLETED, reply_markup=control_keyboard_full)
        user_state.pop(user_id, None)
        return
    try:
        name = POSITIONS[pos]
        duration = DURATIONS_MIN[step-1][pos]
        await bot.send_message(user_id, f"{name} — {format_duration(duration)}", reply_markup=control_keyboard)
        state["position"] += 1
        tasks[user_id] = asyncio.create_task(timer(user_id, duration))
    except IndexError:
        await bot.send_message(user_id, STEP_COMPLETED, reply_markup=control_keyboard_full)

async def timer(user_id, minutes):
    await asyncio.sleep(minutes * 60)
    await start_position(user_id)

@dp.message_handler(lambda m: m.text == "⏭️ Пропустить")
async def skip(message: types.Message):
    user_id = message.chat.id
    task = tasks.pop(user_id, None)
    if task: task.cancel()
    await start_position(user_id)

@dp.message_handler(lambda m: m.text.startswith("↩️ Назад"))
async def go_back(message: types.Message):
    user_id = message.chat.id
    state = user_state.get(user_id)
    if not state:
        return
    if state['step'] <= 2:
        state['step'] = 1
    else:
        state['step'] -= 2
    state['position'] = 0
    await bot.send_message(user_id, f"Шаг {state['step']}")
    await start_position(user_id)

@dp.message_handler(lambda m: m.text == "⛔ Завершить")
async def end_session(message: types.Message):
    user_id = message.chat.id
    task = tasks.pop(user_id, None)
    if task: task.cancel()
    await bot.send_message(user_id, SESSION_DONE, reply_markup=end_keyboard)
    user_state.pop(user_id, None)

@dp.message_handler(lambda m: m.text == "📋 Вернуться к шагам")
async def back_to_steps(message: types.Message):
    user_id = message.chat.id
    task = tasks.pop(user_id, None)
    if task: task.cancel()
    user_state.pop(user_id, None)
    await message.answer("Выбери шаг:", reply_markup=steps_keyboard)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
