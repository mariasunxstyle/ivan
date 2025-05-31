from aiogram import Bot
from steps import POSITIONS, DURATIONS_MIN, get_continue_keyboard, control_keyboard, control_keyboard_full
from timer import user_state, tasks, step_completion_shown
import asyncio

async def start_position(uid, bot: Bot):
    state = user_state.get(uid)
    if not state:
        return
    step = state["step"]
    pos = state["position"]
    if step > 12:
        await bot.send_message(uid, "Ты прошёл(ла) 12 шагов по методу суперкомпенсации ☀️\nКожа адаптировалась. Теперь можно поддерживать загар в своём ритме.", reply_markup=control_keyboard_full)
        return
    try:
        name = POSITIONS[pos]
        dur = DURATIONS_MIN[step - 1][pos]
        text = f"{name} — {int(dur)} мин"
        if name == "Лицом вверх":
            text += "\n↓"
        await bot.send_message(uid, text, reply_markup=control_keyboard)
        message = await bot.send_message(uid, "⏳ Таймер запущен...")

        from timer import run_timer
        tasks[uid] = asyncio.create_task(run_timer(uid, int(dur * 60), message, bot))
    except IndexError:
        if step == 12:
            await bot.send_message(uid, "Ты прошёл(ла) 12 шагов по методу суперкомпенсации ☀️", reply_markup=control_keyboard_full)
        elif uid not in step_completion_shown:
            step_completion_shown.add(uid)
            message = "Шаг завершён. Выбирай ▶️ Продолжить или отдохни ☀️."
            if step <= 2:
                message += "\nЕсли был перерыв — вернись на шаг 1."
            else:
                message += "\nЕсли был перерыв — вернись на 2 шага назад."
            await bot.send_message(uid, message, reply_markup=get_continue_keyboard(step))
