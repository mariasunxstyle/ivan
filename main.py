
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

def format_duration(mins):
    return f"{int(mins)} мин" if mins == int(mins) else f"{int(mins)} мин {int((mins - int(mins))*60)} сек"

steps_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
for i, row in enumerate(DURATIONS_MIN):
    total = sum(row)
    label = f"Шаг {i+1} ({int(total//60)} ч {int(total%60)} мин)" if total >= 60 else f"Шаг {i+1} ({int(total)} мин)"
    steps_keyboard.add(KeyboardButton(label))
steps_keyboard.add(KeyboardButton("ℹ️ Инфо"))

control_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
control_keyboard.add(KeyboardButton("⏭️ Пропустить"))
control_keyboard.add(KeyboardButton("⛔ Завершить"))
control_keyboard.add(KeyboardButton("↩️ Назад на 2 шага (после перерыва)"))
control_keyboard.add(KeyboardButton("📋 Вернуться к шагам"))

control_keyboard_continue = ReplyKeyboardMarkup(resize_keyboard=True)
control_keyboard_continue.add(KeyboardButton("▶️ Продолжить"))
control_keyboard_continue.add(KeyboardButton("📋 Вернуться к шагам"))
control_keyboard_continue.add(KeyboardButton("↩️ Назад на 2 шага (после перерыва)"))
control_keyboard_continue.add(KeyboardButton("⛔ Завершить"))

control_keyboard_full = ReplyKeyboardMarkup(resize_keyboard=True)
control_keyboard_full.add(KeyboardButton("📋 Вернуться к шагам"))
control_keyboard_full.add(KeyboardButton("↩️ Назад на 2 шага (после перерыва)"))
control_keyboard_full.add(KeyboardButton("⛔ Завершить"))

GREETING = "Привет, солнце! ☀️\nТы в таймере по методу суперкомпенсации.\nКожа адаптируется к солнцу постепенно — и загар становится ровным, глубоким и без ожогов.\n\nНачинай с шага 1. Даже если уже немного загорел(а), важно пройти путь с начала.\nКаждый новый день и после перерыва — возвращайся на 2 шага назад.\n\nХочешь подробности — жми /info."
INFO_TEXT = "ℹ️ Инфо\nМетод суперкомпенсации — это безопасный, пошаговый подход к загару.\nОн помогает коже адаптироваться к солнцу, снижая риск ожогов и пятен.\n\nРекомендуем загорать с 7:00 до 11:00 и после 17:00 — в это время солнце мягкое, и при отсутствии противопоказаний можно загорать без SPF.\n\nС 11:00 до 17:00 — солнце более агрессивное. Если остаёшься на улице — надевай одежду, головной убор или используй SPF.\n\nКаждый новый день и после перерыва — возвращайся на 2 шага назад. Это нужно, чтобы кожа не перегружалась и постепенно усиливала защиту.\n\nЕсли есть вопросы — пиши: @sunxbeach_director"

user_state = {}
tasks = {}

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
        dur = DURATIONS_MIN[step-1][pos]
        await bot.send_message(uid, f"{name} — {format_duration(dur)}", reply_markup=control_keyboard)
        state["position"] += 1
        tasks[uid] = asyncio.create_task(timer(uid, int(dur * 60)))
    except IndexError:
        if step == 12:
            await bot.send_message(uid, "Ты прошёл(ла) 12 шагов по методу суперкомпенсации ☀️\nКожа адаптировалась. Теперь можно поддерживать загар в своём ритме.", reply_markup=control_keyboard_full)
        else:
            await bot.send_message(uid, "Шаг завершён. Выбирай продолжить ☀️\nЕсли был перерыв — вернись на 2 шага назад.", reply_markup=control_keyboard_continue)

import time

async def timer(uid, seconds):
    start = time.monotonic()
    while True:
        if time.monotonic() - start >= seconds:
            break
        await asyncio.sleep(1)
    if uid in user_state:
        await start_position(uid)

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
    user_state[uid]["last_step"] = user_state.get(uid, {}).get("step", 1)
    await bot.send_message(uid, "Сеанс завершён. Можешь вернуться позже и начать заново ☀️", reply_markup=control_keyboard_full)

@dp.message_handler(lambda m: m.text.startswith("↩️"))
async def back(msg: types.Message):
    uid = msg.chat.id
    state = user_state.get(uid)
    if not state:
        last = user_state.get(uid, {}).get("last_step", 1)
        user_state[uid] = {"step": 1 if last <= 2 else last - 2, "position": 0}
    else:
        step = state["step"]
        state["step"] = 1 if step <= 2 else step - 2
        state["position"] = 0
    await bot.send_message(uid, f"Шаг {user_state[uid]['step']}")
    await start_position(uid)

@dp.message_handler(lambda m: m.text == "📋 Вернуться к шагам")
async def menu(msg: types.Message):
    uid = msg.chat.id
    t = tasks.pop(uid, None)
    if t: t.cancel()
    user_state.pop(uid, None)
    await msg.answer("Выбери шаг:", reply_markup=steps_keyboard)

@dp.message_handler(lambda m: m.text == "▶️ Продолжить")
async def continue_step(msg: types.Message):
    uid = msg.chat.id
    state = user_state.get(uid)
    if not state:
        return
    state["step"] += 1
    state["position"] = 0
    await bot.send_message(uid, f"Шаг {state['step']}")
    await start_position(uid)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
