
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
        await bot.send_message(uid, f"{name} — {int(dur)} мин")
        if name == "Лицом вверх":
            await bot.send_message(uid, "↓", reply_markup=get_control_keyboard(step))
        state["position"] += 1
        tasks[uid] = asyncio.create_task(run_timer(uid, int(dur * 60), step, pos))
    except IndexError:
        if uid not in step_completion_shown:
            step_completion_shown.add(uid)
            await bot.send_message(uid, f"Шаг {step} завершён.")
            await bot.send_message(uid, "Можешь вернуться позже и начать заново ☀️", reply_markup=get_continue_keyboard(step))

@dp.message_handler(lambda m: m.text == "⛔ Завершить")
async def end(msg: types.Message):
    uid = msg.chat.id
    t = tasks.pop(uid, None)
    if t: t.cancel()
    state = user_state.get(uid, {})
    last_step = state.get("step", 1)
    user_state[uid] = {"last_step": last_step}
    step_completion_shown.discard(uid)
    await bot.send_message(uid, f"Шаг {last_step} завершён.")
    await bot.send_message(uid, "Можешь вернуться позже и начать заново ☀️", reply_markup=end_keyboard)

@dp.message_handler(lambda m: m.text == "↩️ Назад на 2 шага (после перерыва)" or m.text.startswith("↩️ Назад"))
async def back(msg: types.Message):
    uid = msg.chat.id
    state = user_state.get(uid)
    last = state.get("last_step", 1) if state else 1
    new_step = 1 if last <= 2 else last - 2
    user_state[uid] = {"step": new_step, "position": 0}
    step_completion_shown.discard(uid)
    await bot.send_message(uid, f"Шаг {new_step}")
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
    step = state["step"] + 1
    user_state[uid] = {"step": step, "position": 0}
    step_completion_shown.discard(uid)
    await bot.send_message(uid, f"Шаг {step}")
    await start_position(uid)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
