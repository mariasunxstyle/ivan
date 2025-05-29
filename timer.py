import asyncio
import time
from steps import POSITIONS, DURATIONS_MIN, format_duration
from keyboards import get_continue_keyboard, control_keyboard_full
from state import user_state, tasks, step_completion_shown
from texts import GREETING

async def timer(uid, seconds, bot, msg):
    start = time.monotonic()
    bar_states = [
        "☀️🌑🌑🌑🌑🌑🌑🌑🌑🌑", "☀️☀️🌑🌑🌑🌑🌑🌑🌑🌑", "☀️☀️☀️🌑🌑🌑🌑🌑🌑🌑",
        "☀️☀️☀️☀️🌑🌑🌑🌑🌑🌑", "☀️☀️☀️☀️☀️🌑🌑🌑🌑🌑", "☀️☀️☀️☀️☀️☀️🌑🌑🌑🌑",
        "☀️☀️☀️☀️☀️☀️☀️🌑🌑🌑", "☀️☀️☀️☀️☀️☀️☀️☀️🌑🌑",
        "☀️☀️☀️☀️☀️☀️☀️☀️☀️🌑", "☀️☀️☀️☀️☀️☀️☀️☀️☀️☀️"
    ]
    last_state = ""
    while True:
        elapsed = time.monotonic() - start
        remaining = max(0, int(seconds - elapsed))
        percent_done = min(elapsed / seconds, 1.0)
        bar_index = min(int(percent_done * 10), 9)

        bar = bar_states[bar_index]
        minutes = remaining // 60
        seconds_remain = remaining % 60
        time_label = f"{minutes} мин {seconds_remain} сек" if minutes > 0 else f"{seconds_remain} сек"
        text = f"⏳ Осталось: {time_label}\n{bar}"

        if text != last_state:
            try:
                await bot.edit_message_text(
                    text=msg.text.split("\n")[0] + "\n" + text,
                    chat_id=uid,
                    message_id=msg.message_id
                )
            except:
                pass
            last_state = text

        if remaining <= 0:
            break
        await asyncio.sleep(2)

    if uid in user_state:
        await start_position(uid, bot)

async def start_position(uid, bot):
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
        message = await bot.send_message(uid, f"{name} — {format_duration(dur)}\n⏳ Таймер запущен...")
        state["position"] += 1
        tasks[uid] = asyncio.create_task(timer(uid, int(dur * 60), bot, message))
    except IndexError:
        if step == 12:
            await bot.send_message(uid, "Ты прошёл(ла) 12 шагов по методу суперкомпенсации ☀️\nКожа адаптировалась. Теперь можно поддерживать загар в своём ритме.", reply_markup=control_keyboard_full)
        elif uid not in step_completion_shown:
            step_completion_shown.add(uid)
            message = "Шаг завершён. Выбирай ▶️ Продолжить или отдохни ☀️."
            if step <= 2:
                message += "\nЕсли был перерыв — вернись на шаг 1."
            else:
                message += "\nЕсли был перерыв — вернись на 2 шага назад."
            await bot.send_message(uid, message, reply_markup=get_continue_keyboard(step))
