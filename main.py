import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

from steps import POSITIONS, DURATIONS_MIN
from texts import GREETING, INFO_TEXT
from timer import run_timer

API_TOKEN = os.getenv("TOKEN")
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(12):
        mins = sum(DURATIONS_MIN[i])
        button = KeyboardButton(f"Шаг {i+1} — {int(mins)} мин")
        keyboard.add(button)
    keyboard.add(KeyboardButton("ℹ️ Инфо"))
    await message.answer(GREETING, reply_markup=keyboard)

@dp.message_handler(lambda msg: msg.text and msg.text.startswith("Шаг "))
async def start_step(message: types.Message):
    step_num = int(message.text.split()[1]) - 1
    durations = DURATIONS_MIN[step_num]
    for i, pos in enumerate(POSITIONS):
        mins = durations[i]
        if mins == 0:
            continue
        await run_timer(message, pos, mins)
    await message.answer("✅ Шаг завершён! Выбери следующий шаг или вернись назад, если был перерыв.")

@dp.message_handler(lambda msg: msg.text == "ℹ️ Инфо")
async def info(message: types.Message):
    await message.answer(INFO_TEXT)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
