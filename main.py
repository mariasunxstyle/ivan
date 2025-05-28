import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.utils import executor
from handlers import register_handlers
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

register_handlers(dp, bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)