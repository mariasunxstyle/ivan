from aiogram import executor
from bot import dp
import handlers  # noqa

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)