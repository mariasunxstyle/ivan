import asyncio
from bot import bot
from keyboards import get_control_keyboard
from state import user_state, tasks
from texts import POSITIONS, DURATIONS_MIN, format_duration

async def start_position(uid):
    state = user_state.get(uid)
    step = state["step"]
    pos = state["position"]

    if pos >= len(POSITIONS):
        return

    name = POSITIONS[pos]
    dur = DURATIONS_MIN[step - 1][pos]
    message = await bot.send_message(uid, f"{name} — {format_duration(dur)}\n⏳ Таймер запущен...")

    if pos == 0:
        await bot.send_message(uid, "⏰ Управление:", reply_markup=get_control_keyboard(step))

    state["position"] += 1
    tasks[uid] = asyncio.create_task(timer(uid, int(dur * 60), message, bot))

async def timer(uid, duration, msg, bot):
    await asyncio.sleep(duration)
    tasks.pop(uid, None)