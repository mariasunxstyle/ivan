import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

API_TOKEN = os.getenv("TOKEN")
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

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

user_state = {}
tasks = {}
step_completion_shown = set()

def format_duration(minutes):
    return f"{int(minutes)} мин" if minutes == int(minutes) else f"{int(minutes)} мин {int((minutes - int(minutes)) * 60)} сек"

def get_control_keyboard(step):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("⏭️ Пропустить")
    kb.add("⛔ Завершить")
    kb.add("↩️ Назад на 1 шаг" if step <= 2 else "↩️ Назад на 2 шага")
    kb.add("📋 Вернуться к шагам")
    return kb

def get_continue_keyboard(step):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("▶️ Продолжить")
    kb.add("↩️ Назад на 1 шаг" if step <= 2 else "↩️ Назад на 2 шага")
    kb.add("📋 Вернуться к шагам")
    kb.add("⛔ Завершить")
    return kb

@dp.message_handler(lambda m: m.text.startswith("↩️"))
async def back(msg: types.Message):
    uid = msg.chat.id
    task = tasks.pop(uid, None)
    if task:
        task.cancel()
    state = user_state.get(uid, {"step": 1, "position": 0})
    last_step = state.get("step", 1)
    if "1 шаг" in msg.text:
        new_step = max(1, last_step - 1)
    else:
        new_step = max(1, last_step - 2)
    user_state[uid] = {"step": new_step, "position": 0}
    step_completion_shown.discard(uid)
    await bot.send_message(uid, f"Шаг {new_step}")
    await start_position(uid)

async def timer(uid, seconds):
    try:
        await asyncio.sleep(seconds)
        step = user_state.get(uid, {}).get("step", 1)
        step_completion_shown.add(uid)
        text = "Шаг завершён. Выбирай ▶️ Продолжить или отдохни ☀️."
        text += "\nЕсли был перерыв — вернись на шаг 1." if step <= 2 else "\nЕсли был перерыв — вернись на 2 шага назад."
        await bot.send_message(uid, text, reply_markup=get_continue_keyboard(step))
    except asyncio.CancelledError:
        pass

async def start_position(uid):
    state = user_state.get(uid)
    if not state:
        return
    step = state["step"]
    pos = state["position"]
    task = tasks.pop(uid, None)
    if task:
        task.cancel()
    if step > 12:
        await bot.send_message(uid, "Ты прошёл(ла) 12 шагов по методу суперкомпенсации ☀️\nКожа адаптировалась. Теперь можно поддерживать загар в своём ритме.", reply_markup=get_continue_keyboard(step))
        return
    try:
        name = POSITIONS[pos]
        dur = DURATIONS_MIN[step-1][pos]
        state["position"] += 1
        text = f"Шаг {step}\n{name} — {format_duration(dur)}\n⏳ Осталось: {format_duration(dur)}"
        await bot.send_message(uid, text, reply_markup=get_control_keyboard(step))
        tasks[uid] = asyncio.create_task(timer(uid, int(dur * 60)))
    except IndexError:
        if uid not in step_completion_shown:
            step_completion_shown.add(uid)
            text = "Шаг завершён. Выбирай ▶️ Продолжить или отдохни ☀️."
            text += "\nЕсли был перерыв — вернись на шаг 1." if step <= 2 else "\nЕсли был перерыв — вернись на 2 шага назад."
            await bot.send_message(uid, text, reply_markup=get_continue_keyboard(step))

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

@dp.message_handler(lambda m: m.text == "📋 Вернуться к шагам")
async def return_to_steps(msg: types.Message):
    uid = msg.chat.id
    t = tasks.pop(uid, None)
    if t: t.cancel()
    user_state.pop(uid, None)
    step_completion_shown.discard(uid)
    await msg.answer("Выбери шаг:")

@dp.message_handler(lambda m: m.text == "⏭️ Пропустить")
async def skip_position(msg: types.Message):
    uid = msg.chat.id
    t = tasks.pop(uid, None)
    if t:
        t.cancel()
    await start_position(uid)

@dp.message_handler(lambda m: m.text == "⛔ Завершить")
async def end_session(msg: types.Message):
    uid = msg.chat.id
    t = tasks.pop(uid, None)
    if t:
        t.cancel()
    step = user_state.get(uid, {}).get("step", 1)
    state = {"step": step, "position": 0}
    user_state[uid] = state
    step_completion_shown.discard(uid)
    await bot.send_message(uid, "Сеанс завершён. Можешь вернуться позже и начать заново ☀️", reply_markup=get_continue_keyboard(step))

@dp.message_handler(lambda m: m.text.startswith("Шаг "))
async def start_from_step(msg: types.Message):
    try:
        step = int(msg.text.split()[1])
        user_state[msg.chat.id] = {"step": step, "position": 0}
        step_completion_shown.discard(msg.chat.id)
        await bot.send_message(msg.chat.id, f"Шаг {step}")
        await start_position(msg.chat.id)
    except:
        await msg.answer("Не удалось начать шаг. Попробуйте снова.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
