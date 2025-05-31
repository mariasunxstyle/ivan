import asyncio
from keyboards import get_control_keyboard
from state import user_state, step_completion_shown
from steps import STEPS

async def run_timer(bot, chat_id, step_number):
    step_data = next((s for s in STEPS if s["step"] == step_number), None)
    if not step_data:
        return

    for idx, (position, duration) in enumerate(zip(step_data["positions"], step_data["duration_min"])):
        await bot.send_message(chat_id, f"{position} — {int(duration)} мин")

        if idx == 0:
            await bot.send_message(chat_id, "↓", reply_markup=get_control_keyboard(step_number))

        await asyncio.sleep(1)

    if chat_id not in step_completion_shown:
        await bot.send_message(chat_id, "Шаг завершён ☀️")
        step_completion_shown.add(chat_id)
