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
control_keyboard.add(types.KeyboardButton("↩️ Назад на 2 шага"))
control_keyboard.add(types.KeyboardButton("📋 Вернуться к шагам"))

control_keyboard_full = ReplyKeyboardMarkup(resize_keyboard=True)
control_keyboard_full.add(
    types.KeyboardButton("▶️ Продолжить"),
    types.Keyboar

