# main.py для бота SUNXSTYLE

import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils import executor
from handlers import *

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
    await message.answer(GREETING, reply_markup=steps_keyboard)

# Инфо
@dp.message_handler(commands=['info'])
@dp.message_handler(lambda m: m.text == "ℹ️ Инфо")
async def send_info(message: types.Message):
    await message.answer(INFO_TEXT)

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
        await bot.send_message(user_id, ALL_STEPS_DONE_MESSAGE, reply_markup=steps_keyboard)
        user_state.pop(user_id, None)
        return
    try:
        position_name = POSITIONS[pos]
        duration = DURATIONS_MIN[step-1][pos]
        state['position'] += 1
        tasks[user_id] = asyncio.create_task(position_timer(user_id, position_name, duration, step))
    except IndexError:
        await bot.send_message(user_id, STEP_COMPLETED_MESSAGE, reply_markup=complete_keyboard)

# Таймер позиции
async def position_timer(user_id, name, minutes, step):
    await bot.send_message(user_id, f"{name} — {format_duration(minutes)}", reply_markup=control_keyboard)
    await asyncio.sleep(minutes * 60)
    await start_position(user_id)

# Пропустить
@dp.message_handler(lambda m: m.text == "⏭️ Пропустить")
async def skip_position(message: types.Message):
    user_id = message.chat.id
    task = tasks.pop(user_id, None)
    if task:
        task.cancel()
    await start_position(user_id)

# Завершить
@dp.message_handler(lambda m: m.text == "⛔ Завершить")
async def end_session(message: types.Message):
    user_id = message.chat.id
    task = tasks.pop(user_id, None)
    if task:
        task.cancel()
    await bot.send_message(user_id, SESSION_TERMINATED_MESSAGE, reply_markup=steps_keyboard)
    user_state.pop(user_id, None)

# Назад на 2 шага
@dp.message_handler(lambda m: m.text.startswith("↩️"))
async def go_back(message: types.Message):
    user_id = message.chat.id
    state = user_state.get(user_id)
    if not state or state['step'] <= 2:
        await bot.send_message(user_id, BACK_LIMIT_MESSAGE)
        return
    state['step'] -= 2
    state['position'] = 0
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
