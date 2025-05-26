# Финальный main.py с полностью рабочими кнопками управления внутри основного файла
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

def format_duration(min_float):
    minutes = int(min_float)
    seconds = int((min_float - minutes) * 60)
    return f"{minutes} мин" if seconds == 0 else f"{minutes} мин {seconds} сек"

control_keyboard_continue = ReplyKeyboardMarkup(resize_keyboard=True)
control_keyboard_continue.add(KeyboardButton("▶️ Продолжить"))
control_keyboard_continue.add(KeyboardButton("📋 Вернуться к шагам"))
control_keyboard_continue.add(KeyboardButton("↩️ Назад на 2 шага (после перерыва)"))
control_keyboard_continue.add(KeyboardButton("⛔ Завершить"))

control_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
control_keyboard.add(KeyboardButton("⏭️ Пропустить"))
control_keyboard.add(KeyboardButton("⛔ Завершить"))
control_keyboard.add(KeyboardButton("↩️ Назад на 2 шага (после перерыва)"))
control_keyboard.add(KeyboardButton("📋 Вернуться к шагам"))

control_keyboard_full = ReplyKeyboardMarkup(resize_keyboard=True)
control_keyboard_full.add(KeyboardButton("📋 Вернуться к шагам"))
control_keyboard_full.add(KeyboardButton("↩️ Назад на 2 шага (после перерыва)"))
control_keyboard_full.add(KeyboardButton("⛔ Завершить"))

end_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
end_keyboard.add(
    KeyboardButton("📋 Вернуться к шагам"),
    KeyboardButton("↩️ Назад на 2 шага (после перерыва)")
)

steps_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
step_buttons = []
for i, row in enumerate(DURATIONS_MIN):
    min_total = int(sum(row))
    h = min_total // 60
    m = min_total % 60
    label = f"Шаг {i+1} ({f'{h} ч ' if h else ''}{m} мин)"
    step_buttons.append(KeyboardButton(label))
for i in range(0, len(step_buttons), 4):
    steps_keyboard.add(*step_buttons[i:i+4])
steps_keyboard.add(KeyboardButton("ℹ️ Инфо"))

GREETING = """Привет, солнце! ☀️
Ты в таймере по методу суперкомпенсации.
Кожа адаптируется к солнцу постепенно — и загар становится ровным, глубоким и без ожогов.

Метод основан на научных принципах: короткие интервалы активируют выработку меланина и гормонов адаптации.
Такой подход снижает риск ожогов и делает загар устойчивым.

Начинай с шага 1 — даже если уже немного загорел(а).
Каждый новый день и после перерыва — возвращайся на 2 шага назад.

Хочешь подробности — жми /info."""

INFO_TEXT = """ℹ️ Инфо
Метод суперкомпенсации — научно обоснованный способ безопасного загара.
Ты проходишь 12 шагов — каждый с таймингом и сменой позиций.

Как использовать:
1. Начни с шага 1
2. Включи таймер и следуй позициям
3. Каждый новый день и после любого перерыва — возвращайся на 2 шага назад
4. После завершения всех 12 шагов — можешь поддерживать загар в комфортном ритме

Рекомендуем загорать с 7:00 до 11:00 и после 17:00 — в это время солнце мягкое,
и при отсутствии противопоказаний можно загорать без SPF.
С 11:00 до 17:00 — солнце более агрессивное. Если остаёшься на улице —
надевай одежду или используй SPF.

Если есть вопросы — пиши: @sunxbeach_director"""

STEP_COMPLETED = "Шаг завершён. Выбирай следующий или отдохни ☀️\nЕсли был перерыв — вернись на 2 шага назад."

user_state = {}
tasks = {}

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
        await bot.send_message(
            user_id,
            "Ты прошёл(ла) 12 шагов по методу суперкомпенсации ☀️\nКожа адаптировалась. Теперь можно поддерживать загар в своём ритме.",
            reply_markup=control_keyboard_full
        )
        user_state.pop(user_id, None)
        return
    try:
        name = POSITIONS[pos]
        duration = DURATIONS_MIN[step - 1][pos]
        await bot.send_message(user_id, f"{name} — {format_duration(duration)}", reply_markup=control_keyboard)
        state["position"] += 1
        tasks[user_id] = asyncio.create_task(timer(user_id, duration))
    except IndexError:
        if step == 12:
            await bot.send_message(
                user_id,
                "Ты прошёл(ла) 12 шагов по методу суперкомпенсации ☀️\nКожа адаптировалась. Теперь можно поддерживать загар в своём ритме.",
                reply_markup=control_keyboard_full
            )
        else:
            await bot.send_message(user_id, STEP_COMPLETED, reply_markup=control_keyboard_continue)

async def timer(user_id, minutes):
    await asyncio.sleep(minutes * 60)
    await start_position(user_id)

@dp.message_handler(lambda m: m.text == "⏭️ Пропустить")
async def skip(message: types.Message):
    user_id = message.chat.id
    task = tasks.pop(user_id, None)
    if task:
        task.cancel()
    await start_position(user_id)

@dp.message_handler(lambda m: m.text == "⛔ Завершить")
async def end_session(message: types.Message):
    user_id = message.chat.id
    task = tasks.pop(user_id, None)
    if task:
        task.cancel()
    await bot.send_message(user_id, "Сеанс завершён. Можешь вернуться позже и начать заново ☀️", reply_markup=end_keyboard)
    user_state.pop(user_id, None)

@dp.message_handler(lambda m: m.text.startswith("↩️"))
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

@dp.message_handler(lambda m: m.text == "📋 Вернуться к шагам")
async def back_to_steps(message: types.Message):
    user_id = message.chat.id
    task = tasks.pop(user_id, None)
    if task:
        task.cancel()
    user_state.pop(user_id, None)
    await message.answer("Выбери шаг:", reply_markup=steps_keyboard)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
