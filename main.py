# main.py для бота SUNXSTYLE

import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from handlers import (
    steps_keyboard, control_keyboard, control_keyboard_full_vertical, control_keyboard_end,
    POSITIONS, DURATIONS_MIN, format_duration,
    STEP_COMPLETED_MESSAGE, ALL_STEPS_DONE_MESSAGE, SESSION_TERMINATED_MESSAGE,
    GREETING, INFO_TEXT
)

API_TOKEN = os.getenv("TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Хранилище состояния пользователей
user_state = {}
tasks = {}

# Приветствие и старт
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("""Привет, солнце! ☀️
Ты в таймере по методу суперкомпенсации.
Кожа адаптируется к солнцу постепенно — и загар становится ровным, глубоким и без ожогов.

Метод основан на научных принципах: короткие интервалы активируют выработку меланина и гормонов адаптации.
Такой подход снижает риск ожогов и делает загар устойчивым.

Начинай с шага 1 — даже если уже немного загорел(а).
Каждый новый день и после любого перерыва — возвращайся на 2 шага назад.

Хочешь подробности — жми /info.", reply_markup=steps_keyboard)

# Инфо
@dp.message_handler(commands=['info'])
@dp.message_handler(lambda m: m.text == "ℹ️ Инфо")
async def send_info(message: types.Message):
    await message.answer("""ℹ️ Инфо
Метод суперкомпенсации — научно обоснованный способ безопасного загара.
Ты проходишь 12 шагов — каждый с таймингом и сменой позиций.

Как использовать:
1. Начни с шага 1
2. Включи таймер и следуй позициям
3. Каждый новый день и после любого перерыва — возвращайся на 2 шага назад
4. После завершения всех 12 шагов — можешь поддерживать загар в комфортном ритме

Рекомендуем загорать с 7:00 до 11:00 и после 17:00 — в это время солнце мягкое, и при отсутствии противопоказаний можно загорать без SPF.
С 11:00 до 17:00 — солнце более агрессивное. Если остаёшься на улице — надевай одежду или используй SPF.

Если есть вопросы — пиши: @sunxbeach_director""")

# Обработка выбора шага
@dp.message_handler(lambda m: m.text.startswith("Шаг "))
async def handle_step(message: types.Message):
    user_id = message.chat.id
    step_num = int(message.text.split()[1])
    user_state[user_id] = {"step": step_num, "position": 0}
    await start_position(user_id)

# Начать позицию с таймером
async def start_position(user_id):
    state = user_state.get(user_id)
    if not state:
        return
    step = state['step']
    pos = state['position']
    if step > 12:
        await bot.send_message(user_id, ALL_STEPS_DONE_MESSAGE, reply_markup=control_keyboard_end)
        user_state.pop(user_id, None)
        return
    try:
        position_name = POSITIONS[pos]
        duration = DURATIONS_MIN[step - 1][pos]
        state['position'] += 1
        tasks[user_id] = asyncio.create_task(position_timer(user_id, position_name, duration, step))
    except IndexError:
        await bot.send_message(user_id, STEP_COMPLETED_MESSAGE, reply_markup=control_keyboard_full_vertical)

# Таймер позиции
async def position_timer(user_id, name, minutes, step):
    await bot.send_message(user_id, f"{name} — {format_duration(minutes)}", reply_markup=control_keyboard)
    await asyncio.sleep(minutes * 60)
    state = user_state.get(user_id)
    if state and state['position'] >= len(POSITIONS):
        await bot.send_message(user_id, STEP_COMPLETED_MESSAGE, reply_markup=control_keyboard_full_vertical)
    else:
        await start_position(user_id)

# Пропустить
@dp.message_handler(lambda m: m.text == "⏭️ Пропустить")
async def skip_position(message: types.Message):
    user_id = message.chat.id
    task = tasks.pop(user_id, None)
    if task:
        task.cancel()
    state = user_state.get(user_id)
    if state and state['position'] >= len(POSITIONS):
        await bot.send_message(user_id, STEP_COMPLETED_MESSAGE, reply_markup=control_keyboard_full_vertical)
    else:
        await start_position(user_id)

# Завершить
@dp.message_handler(lambda m: m.text == "⛔ Завершить")
async def end_session(message: types.Message):
    user_id = message.chat.id
    task = tasks.pop(user_id, None)
    if task:
        task.cancel()
    await bot.send_message(user_id, STEP_COMPLETED_MESSAGE, reply_markup=control_keyboard_end)
    user_state.pop(user_id, None)

# Назад на 2 шага
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
    step_num = state['step']
    await bot.send_message(user_id, f"Шаг {step_num}")
    await asyncio.sleep(0.5)
    await start_position(user_id)

# Вернуться к шагам
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

