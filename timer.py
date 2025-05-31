import asyncio
from aiogram import types

async def run_timer(message: types.Message, position: str, minutes: float):
    await message.answer(f"{position} — {int(minutes)} мин\n⏳ Таймер запущен...")
    await asyncio.sleep(int(minutes * 60))
