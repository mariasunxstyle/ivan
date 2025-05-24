
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.callback_data import CallbackData
import asyncio
import logging
import os

from steps import steps_data
from handlers import register_handlers

API_TOKEN = os.getenv("TOKEN")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

register_handlers(dp)

def get_step_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    for step in steps_data:
        duration = step['duration_min']
        h, m = divmod(duration, 60)
        if h > 0:
            label = f"Шаг {step['step']} — {h}ч {m}м"
        else:
            label = f"Шаг {step['step']} — {m}м"
        keyboard.insert(KeyboardButton(label))
    keyboard.add(KeyboardButton("ℹ️ Инфо"))
    return keyboard

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
