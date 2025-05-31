import asyncio
from aiogram import Bot
from aiogram.types import BotCommand
import os
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("TOKEN")
bot = Bot(token=API_TOKEN)

async def set_commands():
    await bot.set_my_commands([
        BotCommand("start", "Запустить таймер"),
        BotCommand("info", "Инфо о методе")
    ])
    print("Меню установлено")

if __name__ == '__main__':
    asyncio.run(set_commands())
