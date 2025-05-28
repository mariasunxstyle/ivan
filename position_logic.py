import asyncio
from bot import bot
from keyboards import POSITIONS, DURATIONS_MIN, format_duration, get_control_keyboard, get_continue_keyboard, control_keyboard_full
from state import user_state, tasks, step_completion_shown
import timer

async def start_position(uid):
    state = user_state.get(uid)
    if not state:
        return

    step = state["step"]
    pos = state["position"]

    if step > 12:
        await bot.send_message(
            uid,
            "Ты прошёл(ла) 12 шагов по методу суперкомпенсации ☀️\nКожа адаптировалась. Теперь можно поддерживать загар в своём ритме.",
            reply_markup=control_keyboard_full
        )
        return

    try:
        name = POSITIONS[pos]
        dur = DURATIONS_MIN[step-1][pos]

        await bot.send_message(uid, name)
        message = await bot.send_message(
            uid,
            f"{name} — ⏳ Осталось: {format_duration(dur)}",
            reply_markup=get_control_keyboard(step)
        )

        state["position"] += 1
        tasks[uid] = asyncio.create_task(timer.timer(uid, int(dur * 60), message, start_position, name))

    except IndexError:
        if step == 12:
            await bot.send_message(
                uid,
                "Ты прошёл(ла) 12 шагов по методу суперкомпенсации ☀️\nКожа адаптировалась. Теперь можно поддерживать загар в своём ритме.",
                reply_markup=control_keyboard_full
            )
        elif uid not in step_completion_shown:
            step_completion_shown.add(uid)
            message = "Шаг завершён. Выбирай ▶️ Продолжить или отдохни ☀️."
            message += "\nЕсли был перерыв — вернись на шаг 1." if step <= 2 else "\nЕсли был перерыв — вернись на 2 шага назад."
            await bot.send_message(uid, message, reply_markup=get_continue_keyboard(step))
