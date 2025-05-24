from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio
import os

from keyboards import get_step_keyboard, get_control_keyboard, get_post_step_keyboard
from utils import is_subscribed
from steps import steps, positions_by_step
from handlers import register_handlers

API_TOKEN = os.getenv("TOKEN")
CHANNEL = "@sunxstyle"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

register_handlers(dp)

state = {}

# Приветствие и инфо
WELCOME = (
    "Привет, солнце! ☀️\n"
    "Ты в таймере по методу суперкомпенсации.\n"
    "Кожа адаптируется к солнцу постепенно — и загар получается ровным, глубоким и без ожогов.\n\n"
    "Метод основан на научных принципах: короткие интервалы активируют выработку меланина и гормонов адаптации.\n"
    "Такой подход снижает риск ожогов и делает загар устойчивым.\n\n"
    "Начинай с шага 1 — даже если уже немного загорел(а).\n"
    "Каждый новый день и после перерыва — возвращайся на 2 шага назад.\n\n"
    "Хочешь подробности — жми /info."
)

INFO = (
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

async def tell_position(chat_id: int, step: int, pos_index: int):
    name, mins = positions_by_step[step][pos_index]
    await bot.send_message(chat_id, f"{name} — {mins} мин", reply_markup=get_control_keyboard())
