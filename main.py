import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

from keyboards import steps_keyboard, get_control_keyboard, get_continue_keyboard, end_keyboard
from state import user_state, tasks, step_completion_shown
from steps import STEPS
from timer import run_timer
from texts import WELCOME_TEXT, INFO_TEXT

API_TOKEN = os.getenv("TOKEN")
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer(WELCOME_TEXT, reply_markup=steps_keyboard())

@dp.message_handler(commands=["info"])
async def cmd_info(message: types.Message):
    await message.answer(INFO_TEXT, reply_markup=steps_keyboard())

@dp.message_handler(lambda msg: msg.text.startswith("Шаг"))
async def handle_step(msg: types.Message):
    try:
        step_number = int(msg.text.split()[1])
        user_state[msg.chat.id] = {"step": step_number, "position": 0}
        step_completion_shown[msg.chat.id] = False
        await start_position(msg.chat.id, bot)
    except Exception as e:
        logging.error(f"Ошибка запуска шага: {e}")

@dp.message_handler(lambda msg: msg.text == "⏭️ Пропустить")
async def skip_position(msg: types.Message):
    state = user_state.get(msg.chat.id)
    if not state:
        return
    state["position"] += 1
    await start_position(msg.chat.id, bot)

@dp.message_handler(lambda msg: msg.text == "⛔ Завершить")
async def finish_session(msg: types.Message):
    tasks.pop(msg.chat.id, None)
    step_completion_shown[msg.chat.id] = True
    await msg.answer(
        "Сеанс завершён. Можешь вернуться позже и начать заново ☀️",
        reply_markup=end_keyboard()
    )

@dp.message_handler(lambda msg: msg.text.startswith("↩️ Назад"))
async def go_back_two_steps(msg: types.Message):
    state = user_state.get(msg.chat.id)
    if not state:
        return
    new_step = max(1, state["step"] - 2)
    user_state[msg.chat.id] = {"step": new_step, "position": 0}
    step_completion_shown[msg.chat.id] = False
    await start_position(msg.chat.id, bot)

@dp.message_handler(lambda msg: msg.text == "📋 Вернуться к шагам")
async def back_to_steps(msg: types.Message):
    tasks.pop(msg.chat.id, None)
    await msg.answer("Выбери шаг:", reply_markup=steps_keyboard())

@dp.message_handler(lambda msg: msg.text == "▶️ Продолжить")
async def continue_step(msg: types.Message):
    state = user_state.get(msg.chat.id)
    if not state:
        return
    await start_position(msg.chat.id, bot)

async def start_position(uid, bot):
    state = user_state.get(uid)
    if not state:
        return
    step = state["step"]
    position = state["position"]

    if step > len(STEPS):
        await bot.send_message(uid, "Ты прошёл(ла) 12 шагов по методу суперкомпенсации ☀️\nКожа адаптировалась. Теперь можно поддерживать загар в своём ритме.", reply_markup=end_keyboard())
        return

    if position >= len(STEPS[step - 1]["positions"]):
        if not step_completion_shown.get(uid):
            step_completion_shown[uid] = True
            await bot.send_message(uid,
                "Шаг завершён. Выбирай ▶️ Продолжить или отдохни ☀️.\nЕсли был перерыв — вернись на 2 шага назад.",
                reply_markup=get_continue_keyboard(step)
            )
        return

    pos = STEPS[step - 1]["positions"][position]
    dur = STEPS[step - 1]["duration_min"][position]
    msg = await bot.send_message(uid, f"{pos} — {int(dur)} мин", reply_markup=get_control_keyboard(step))
    tasks[uid] = asyncio.create_task(run_timer(bot, msg, dur * 60, uid))

