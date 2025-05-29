import asyncio
from aiogram.types import Message
from keyboards import get_control_keyboard
from state import user_state, tasks

POSITIONS = ["Лицом вверх", "На животе", "Левый бок", "Правый бок", "В тени"]
from steps import DURATIONS_MIN

def format_duration(minutes):
    if minutes >= 60:
        hours = int(minutes) // 60
        mins = int(minutes) % 60
        return f"{hours} ч {mins} мин" if mins else f"{hours} ч"
    return f"{int(minutes)} мин"

async def start_position(uid):
    state = user_state.get(uid)
    if not state:
        last = user_state.get(uid, {}).get("last_step", 1)
        user_state[uid] = {"step": 1, "position": 0} if last <= 2 else {"step": last - 2, "position": 0}
        state = user_state[uid]

    step = state["step"]
    pos = state["position"]

    if step > 12 or pos >= 5:
        return

    name = POSITIONS[pos]
    dur = DURATIONS_MIN[step - 1][pos]
    duration_sec = int(dur * 60)

    text = f"{name} — {format_duration(dur)}\n⏳ Таймер запущен..."
    message = await tasks[uid].bot.send_message(uid, text)
    if pos == 0:
        await tasks[uid].bot.send_message(uid, "⏰ Управление:", reply_markup=get_control_keyboard(step))

    tasks[uid] = asyncio.create_task(timer(uid, duration_sec, message, tasks[uid].bot))

async def timer(uid, duration, msg: Message, bot):
    message_id = msg.message_id
    chat_id = msg.chat.id
    bar_length = 12

    for remaining in range(duration, 0, -1):
        time_label = f"{remaining // 60}:{remaining % 60:02d}"
        percent = (duration - remaining) / duration
        filled = int(bar_length * percent)
        bar = "▓" * filled + "░" * (bar_length - filled)
        text = f"{msg.text.split('\n')[0]}\n⏳ Осталось: {time_label}\n{bar}"
        try:
            await bot.edit_message_text(text, chat_id, message_id)
        except:
            pass
        await asyncio.sleep(1)

    await bot.edit_message_text(f"{msg.text.split('\n')[0]}\n⏳ Таймер завершён.", chat_id, message_id)
    tasks.pop(uid, None)