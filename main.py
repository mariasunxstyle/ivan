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

bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

register_handlers(dp)

state = {}

async def tell_position(chat_id: int, step: int, pos_index: int):
    name, mins = positions_by_step[step][pos_index]
    await bot.send_message(chat_id, f"{name} — {mins} мин", reply_markup=get_control_keyboard())

async def pos_timer():
    while True:
        await asyncio.sleep(60)
        for chat_id in list(state.keys()):
            usr = state[chat_id]
            step = usr["step"]
            name, mins = positions_by_step[step][usr["pos_index"]]
            usr.setdefault("elapsed", 0)
            usr["elapsed"] += 1
            if usr["elapsed"] >= mins:
                usr["elapsed"] = 0
                await advance_position(chat_id)

async def on_startup(dp):
    print("Bot started")
    asyncio.create_task(pos_timer())

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
