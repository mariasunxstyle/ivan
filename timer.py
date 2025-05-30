import asyncio
import time
from state import user_state, tasks
from keyboards import get_control_keyboard, get_continue_keyboard, control_keyboard_full
from aiogram import Bot

POSITIONS = ["Лицом вверх", "На животе", "Левый бок", "Правый бок", "В тени"]

DURATIONS_MIN = [
    [1.5, 1.5, 1.0, 1.0, 3.0],
    [2.0, 2.0, 1.0, 1.0, 3.0],
    [3.0, 3.0, 1.5, 1.5, 5.0],
    [5.0, 5.0, 2.5, 2.5, 5.0],
    [7.0, 7.0, 3.0, 3.0, 7.0],
    [9.0, 9.0, 5.0, 5.0, 10.0],
    [12.0, 12.0, 7.0, 7.0, 10.0],
    [15.0, 15.0, 10.0, 10.0, 10.0],
    [20.0, 20.0, 15.0, 15.0, 15.0],
    [25.0, 25.0, 20.0, 20.0, 20.0],
    [35.0, 35.0, 25.0, 25.0, 30.0],
    [45.0, 45.0, 30.0, 30.0, 40.0],
]

step_completion_shown = set()

def format_duration(mins):
    return f"{int(mins)} мин" if mins == int(mins) else f"{int(mins)} мин {int((mins - int(mins)) * 60)} сек"

async def start_position(bot: Bot, uid: int):
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
        dur = DURATIONS_MIN[step-1][pos]
        message = await bot.send_message(uid, f"{name} — {format_duration(dur)}\n⏳ Таймер запущен...")
        state["position"] += 1
        tasks[uid] = asyncio.create_task(timer(bot, uid, int(dur * 60), message))
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

async def timer(bot: Bot, uid: int, seconds: int, msg):
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
                await bot.edit_message_text(text=msg.text.split("\n")[0] + "\n" + text, chat_id=uid, message_id=msg.message_id)
            except:
                pass
            last_state = text

        if remaining <= 0:
            break
        await asyncio.sleep(2)

    if uid in user_state:
        await start_position(bot, uid)