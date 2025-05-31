
import asyncio
from aiogram import types
from keyboards import get_control_keyboard
from state import tasks, user_state, step_completion_shown

async def timer(bot, chat_id, step_index, position_index, duration_min):
    total_seconds = int(duration_min * 60)
    for remaining in range(total_seconds, 0, -1):
        if chat_id not in tasks or tasks[chat_id].cancelled():
            return
        minutes, seconds = divmod(remaining, 60)
        bar_length = 20
        filled = bar_length - int((remaining / total_seconds) * bar_length)
        progress_bar = '▮' * filled + '▯' * (bar_length - filled)
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=tasks[chat_id].message_id,
            text=f"⏳ {progress_bar}  {minutes:02}:{seconds:02}"
        )
        await asyncio.sleep(1)

    await bot.send_message(chat_id, f"Шаг {step_index + 1} завершён ☀️", reply_markup=get_control_keyboard())
    step_completion_shown.add(chat_id)

run_timer = timer
