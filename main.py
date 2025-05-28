import asyncio
from aiogram import executor
from bot import dp
import handlers  # noqa

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    executor.start_polling(dp, skip_updates=True)
