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

ALL_STEPS_DONE_MESSAGE = (
    "Ты завершил(а) все 12 шагов по методу суперкомпенсации!\n"
    "Кожа адаптировалась — теперь можешь поддерживать загар в комфортном ритме ☀️"
)
SESSION_TERMINATED_MESSAGE = (
    "Сеанс завершён.\nМожешь вернуться позже и начать заново ☀️"
)

# Приветствие и старт
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    welcome_text = (
        "Привет, солнце! ☀️\n"
        "Ты в таймере по методу суперкомпенсации.\n"
        "Кожа адаптируется к солнцу постепенно — и загар получается ровным, глубоким и без ожогов.\n\n"
        "Метод основан на научных принципах: короткие интервалы активируют выработку меланина и гормонов адаптации.\n"
        "Такой подход снижает риск ожогов и делает загар устойчивым.\n\n"
        "Начинай с шага 1 — даже если уже немного загорел(а).\n"
        "Каждый новый день и после перерыва — возвращайся на 2 шага назад.\n\n"
        "Хочешь подробности — жми /info."
    )
    await message.answer(welcome_text, reply_markup=steps_keyboard)

# Инфо
@dp.message_handler(commands=['info'])
@dp.message_handler(lambda m: m.text == "ℹ️ Инфо")
async def send_info(message: types.Message):
    info_text = (
        "ℹ️ Инфо\n"
        "Метод суперкомпенсации — научно обоснованный способ безопасного загара.\n"
        "Ты проходишь 12 шагов — каждый с таймингом и сменой позиций.\n\n"
        "Как использовать:\n"
        "1. Начни с шага 1\n"
        "2. Включи таймер и следуй позициям\n"
        "3. Каждый новый день — возвращайся на 2 шага назад\n"
        "4. После завершения всех 12 шагов — можешь поддерживать загар в комфортном ритме\n\n"
        "Рекомендуем загорать с 7:00 до 11:00 и после 17:00 — в это время солнце мягкое, и при отсутствии противопоказаний можно загорать без SPF.\n"
        "С 11:00 до 17:00 — солнце более агрессивное. Если остаёшься на улице — надевай одежду или используй SPF.\n\n"
        "Если есть вопросы — пиши: @sunxbeach_director"
    )
    await message.answer(info_text)

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
        duration = DURATIONS_MIN[step-1][pos]
        state['position'] += 1
        tasks[user_id] = asyncio.create_task(position_timer(user_id, position_name, duration, step))
    except IndexError:
        await bot.send_message(user_id, "Шаг завершён!", reply_markup=complete_keyboard)

# Таймер позиции
async def position_timer(user_id, name, minutes, step):
    await bot.send_message(user_id, f"{name} — {format_duration(minutes)}", reply_markup=control_keyboard)
    await asyncio.sleep(minutes * 60)
    state = user_state.get(user_id)
    if state and state['position'] >= len(POSITIONS):
        await bot.send_message(user_id, "Шаг завершён!", reply_markup=complete_keyboard)
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
        await bot.send_message(user_id, "Шаг завершён!", reply_markup=complete_keyboard)
    else:
        await start_position(user_id)

# Завершить
@dp.message_handler(lambda m: m.text == "⛔ Завершить")
async def end_session(message: types.Message):
    user_id = message.chat.id
    task = tasks.pop(user_id, None)
    if task:
        task.cancel()
    await bot.send_message(user_id, "Шаг завершён!", reply_markup=control_keyboard_end)
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
