import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

from steps import steps_keyboard, get_continue_keyboard, get_control_keyboard, control_keyboard_full, end_keyboard, POSITIONS, DURATIONS_MIN
from texts import GREETING, INFO_TEXT
from timer import run_timer, user_state, tasks, step_completion_shown

API_TOKEN = os.getenv("TOKEN")
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(msg: types.Message):
    await msg.answer(GREETING, reply_markup=steps_keyboard)

@dp.message_handler(commands=['info'])
@dp.message_handler(lambda m: m.text == "ℹ️ Инфо")
async def info(msg: types.Message):
    await msg.answer(INFO_TEXT)

@dp.message_handler(lambda m: m.text.startswith("Шаг "))
async def handle_step(msg: types.Message):
    step = int(msg.text.split()[1])
    user_state[msg.chat.id] = {"step": step, "position": 0}
    step_completion_shown.discard(msg.chat.id)
    await start_position(msg.chat.id)

async def start_position(uid):
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
        message = await bot.send_message(uid, f"{name} — {int(dur)} мин\n⏳ Таймер запущен...")
        state["position"] += 1
        tasks[uid] = asyncio.create_task(run_timer(uid, int(dur * 60), message, bot))
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

@dp.message_handler(lambda m: m.text == "⏭️ Пропустить")
async def skip(msg: types.Message):
    uid = msg.chat.id
    t = tasks.pop(uid, None)
    if t: t.cancel()
    await start_position(uid)

@dp.message_handler(lambda m: m.text == "⛔ Завершить")
async def end(msg: types.Message):
    uid = msg.chat.id
    t = tasks.pop(uid, None)
    if t: t.cancel()
    user_state[uid] = {"last_step": user_state.get(uid, {}).get("step", 1)}
    step_completion_shown.discard(uid)
    await bot.send_message(uid, "Сеанс завершён. Можешь вернуться позже и начать заново ☀️", reply_markup=end_keyboard)

@dp.message_handler(lambda m: m.text.startswith("↩️"))
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

@dp.message_handler(lambda m: m.text == "📋 Вернуться к шагам")
async def menu(msg: types.Message):
    uid = msg.chat.id
    t = tasks.pop(uid, None)
    if t: t.cancel()
    user_state.pop(uid, None)
    step_completion_shown.discard(uid)
    await msg.answer("Выбери шаг:", reply_markup=steps_keyboard)

@dp.message_handler(lambda m: m.text == "▶️ Продолжить")
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

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
