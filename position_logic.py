from keyboards import get_control_keyboard
from timer import run_timer

async def send_position_with_timer(bot, uid, name, dur, step, user_state, start_position, tasks):
    # Отправить позицию
    await bot.send_message(uid, f"{name} — {int(dur)} мин", reply_markup=None)
    # Отправить таймер
    message = await bot.send_message(
        uid,
        "⏳ Таймер запущен...",
        reply_markup=get_control_keyboard(step)
    )
    tasks[uid] = asyncio.create_task(
        run_timer(bot, uid, int(dur * 60), message, user_state, start_position, step)
    )