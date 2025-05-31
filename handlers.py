
import asyncio
from aiogram import types
from steps import POSITIONS, DURATIONS_MIN, get_control_keyboard, get_continue_keyboard, control_keyboard_full, steps_keyboard, end_keyboard
from timer import run_timer, user_state, tasks, step_completion_shown

bot = None  # будет установлен из main.py
start_position_callback = None  # экспортируемый указатель

async def start_position(uid):
    state = user_state.get(uid)
    if not state:
        return

    step = state["step"]
    pos = state["position"]

    if step > 12:
        await bot.send_message(
            uid,
            "Ты прошёл(ла) 12 шагов по методу суперкомпенсации ☀️\n"
            "Кожа адаптировалась. Теперь можно поддерживать загар в своём ритме.",
            reply_markup=control_keyboard_full
        )
        return

    try:
        name = POSITIONS[pos]
        dur = DURATIONS_MIN[step - 1][pos]
        text = f"{name} — {int(dur)} мин\n⏳ Таймер запущен..."

        prev_task = tasks.pop(uid, None)
        if prev_task:
            prev_task.cancel()
            try:
                await prev_task
            except asyncio.CancelledError:
                pass

        message = await bot.send_message(uid, text, reply_markup=get_control_keyboard(step))
        if name == "Лицом вверх":
            await bot.send_message(uid, "↓")

        state["position"] += 1
        tasks[uid] = asyncio.create_task(run_timer(uid, int(dur * 60), message, bot))

    except IndexError:
        if step == 12:
            await bot.send_message(
                uid,
                "Ты прошёл(ла) 12 шагов по методу суперкомпенсации ☀️\n"
                "Кожа адаптировалась. Теперь можно поддерживать загар в своём ритме.",
                reply_markup=control_keyboard_full
            )
        elif uid not in step_completion_shown:
            step_completion_shown.add(uid)
            msg = "Шаг завершён. Выбирай ▶️ Продолжить или отдохни ☀️."
            if step <= 2:
                msg += "\nЕсли был перерыв — вернись на шаг 1."
            else:
                msg += "\nЕсли был перерыв — вернись на 2 шага назад."
            await bot.send_message(uid, msg, reply_markup=get_continue_keyboard(step))

async def skip(msg: types.Message):
    uid = msg.chat.id
    t = tasks.pop(uid, None)
    if t: t.cancel()
    await start_position(uid)

async def end(msg: types.Message):
    uid = msg.chat.id
    t = tasks.pop(uid, None)
    if t: t.cancel()
    user_state[uid] = {"last_step": user_state.get(uid, {}).get("step", 1)}
    step_completion_shown.discard(uid)
    step = user_state.get(uid, {}).get("step", "?")
    await bot.send_message(uid, f"Шаг {step} завершён.")
    await bot.send_message(uid, "Сеанс завершён. Можешь вернуться позже и начать заново ☀️", reply_markup=end_keyboard)

async def back(msg: types.Message):
    uid = msg.chat.id
    state = user_state.get(uid)
    if not state:
        last = user_state.get(uid, {}).get("last_step", 1)
        user_state[uid] = {"step": 1, "position": 0} if last <= 2 else {"step": last - 2, "position": 0}
    else:
        step = state["step"]
        state["step"] = 1 if step <= 2 else step - 2
        state["position"] = 0
    step_completion_shown.discard(uid)
    await bot.send_message(uid, f"Шаг {user_state[uid]['step']}")
    await start_position(uid)

async def menu(msg: types.Message):
    uid = msg.chat.id
    t = tasks.pop(uid, None)
    if t: t.cancel()
    user_state.pop(uid, None)
    step_completion_shown.discard(uid)
    await msg.answer("Выбери шаг:", reply_markup=steps_keyboard)

async def continue_step(msg: types.Message):
    uid = msg.chat.id
    state = user_state.get(uid)
    if not state:
        return
    state["step"] += 1
    state["position"] = 0
    step_completion_shown.discard(uid)
    await bot.send_message(uid, f"Шаг {state['step']}")
    await start_position(uid)
