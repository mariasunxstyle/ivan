from aiogram import types
from aiogram.dispatcher import Dispatcher
from userlog import get_all_users, get_recent_users

def setup(dp: Dispatcher):
    @dp.message_handler(commands=['stats'])
    async def send_stats(msg: types.Message):
        all_users = get_all_users()
        recent = get_recent_users()
        text = (
            f"Всего пользователей: {len(all_users)}\n"
            f"Активны сегодня: {len(recent)}\n"
        )
        if recent:
            text += "Последние: " + ", ".join(recent)
        await msg.answer(text)
