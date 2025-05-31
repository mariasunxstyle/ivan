
import asyncio
from aiogram import types
from bot import bot
from keyboards import get_control_keyboard
from state import user_state, tasks, step_completion_shown
from texts import steps_data

async def run_timer(uid, step_number):
    state = user_state.get(uid)
    if not state:
        return

    positions = steps_data[step_number - 1]['positions']
    durations = steps_data[step_number - 1]['duration_min']

    for i, (position, duration) in enumerate(zip(positions, durations)):
        if state.get("cancelled"):
            return

        state["position"] = i
        keyboard = get_control_keyboard(step_number)

        text = f"{position} — {duration} мин"
        if i == 0:
            text += "

↓"

        await bot.send_message(uid, text, reply_markup=keyboard)
        await asyncio.sleep(duration * 60)

    step_completion_shown.add(uid)
    await bot.send_message(uid, "Шаг завершён ☀️")
    back_button = get_control_keyboard(step_number, after_step=True)
    await bot.send_message(uid, "Можешь вернуться позже и начать заново.", reply_markup=back_button)
