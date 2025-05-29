from keyboards import get_control_keyboard
from timer import run_timer

async def send_position_with_timer(bot, uid, name, dur, step, user_state, start_position, tasks):
    # Отправить позицию отдельно
    await bot.send_message(uid, f"{name} — {int(dur)} мин")
    # Затем таймер
    message = await bot.send_message(
        uid,
        "⏳ Осталось: ...",
        reply_markup=get_control_keyboard(step)
    )
    tasks[uid] = asyncio.create_task(
        run_timer(bot, uid, int(dur * 60), message, user_state, start_position, step)
    )