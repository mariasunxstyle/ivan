import asyncio
from bot import bot, dp
from handlers import *
from aiogram import executor

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
