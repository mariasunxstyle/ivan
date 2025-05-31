from aiogram import types
from userlog import get_all_users, get_recent_users

async def stats_command(msg: types.Message):
    users = get_all_users()
    recent = get_recent_users()
    text = f"Всего пользователей: {len(users)}"
    if recent:
        text += f"\nПоследние активные: {', '.join(recent)}"
    await msg.answer(text)
