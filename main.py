import asyncio
import logging
import os
import time
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
    [45.0, 45.0, 30.0, 30.0, 40.0]
]

def format_duration(mins):
    return f"{int(mins)} мин" if mins == int(mins) else f"{int(mins)} мин {int((mins - int(mins)) * 60)} сек"

steps_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
for i, row in enumerate(DURATIONS_MIN):
    total = sum(row)
    h = int(total // 60)
    m = int(total % 60)
    label = f"Шаг {i + 1} ({f'{h} ч ' if h else ''}{m} мин)"
    steps_keyboard.insert(KeyboardButton(label))
steps_keyboard.add(KeyboardButton("ℹ️ Инфо"))

def get_control_keyboard(step):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("⏭️ Пропустить"))
    kb.add(KeyboardButton("⛔ Завершить"))
    if step <= 2:
        kb.add(KeyboardButton("↩️ Назад на шаг 1 (если был перерыв)"))
    else:
        kb.add(KeyboardButton("↩️ Назад на 2 шага (после перерыва)"))
    kb.add(KeyboardButton("📋 Вернуться к шагам"))
    return kb

def get_continue_keyboard(step):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("▶️ Продолжить"))
    kb.add(KeyboardButton("📋 Вернуться к шагам"))
    if step <= 2:
        kb.add(KeyboardButton("↩️ Назад на шаг 1 (если был перерыв)"))
    else:
        kb.add(KeyboardButton("↩️ Назад на 2 шага (после перерыва)"))
    return kb

def get_end_keyboard(step):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("📋 Вернуться к шагам"))
    kb.add(KeyboardButton("↩️ Назад на 2 шага (после перерыва)"))
    return kb

@dp.message_handler(commands=['start'])
async def send_welcome(msg: types.Message):
    await msg.answer("Привет, солнце! ☀️\nТы в таймере по методу суперкомпенсации.\nКожа адаптируется к солнцу постепенно — и загар получается ровным, глубоким и без ожогов.\n\nМетод основан на научных принципах: короткие интервалы активируют выработку меланина и гормонов адаптации.\nТакой подход снижает риск ожогов и делает загар устойчивым.\n\nНачинай с шага 1 — даже если уже немного загорел(а).\nКаждый новый день и после перерыва — возвращайся на 2 шага назад.\n\nХочешь подробности — жми /info.", reply_markup=steps_keyboard)

@dp.message_handler(commands=['info'])
@dp.message_handler(lambda m: m.text == "ℹ️ Инфо")
async def info(msg: types.Message):
    await msg.answer("ℹ️ Инфо\nМетод суперкомпенсации — научно обоснованный способ безопасного загара.\nТы проходишь 12 шагов — каждый с таймингом и сменой позиций.\n\nКак использовать:\n1. Начни с шага 1\n2. Включи таймер и следуй позициям\n3. Каждый новый день и после любого перерыва — возвращайся на 2 шага назад\n4. После завершения всех 12 шагов — можешь поддерживать загар в комфортном ритме\n\nРекомендуем загорать с 7:00 до 11:00 и после 17:00 — в это время солнце мягкое,\nи при отсутствии противопоказаний можно загорать без SPF.\nС 11:00 до 17:00 — солнце более агрессивное. Если остаёшься на улице —\nнадевай одежду или используй SPF.\n\nЕсли есть вопросы — пиши: @sunxbeach_director")
@dp.message_handler(lambda m: m.text.startswith("Шаг "))
async def handle_step(msg: types.Message):
    uid = msg.chat.id
    t = tasks.pop(uid, None)
    if t: t.cancel()
    step = int(msg.text.split()[1])
    if step > 12:
        await bot.send_message(uid, "Ты прошёл(ла) 12 шагов по методу суперкомпенсации ☀️\nКожа адаптировалась. Теперь можно поддерживать загар в своём ритме.", reply_markup=get_end_keyboard(12))
        return
    user_state[uid] = {"step": step, "position": 0}
    step_completion_shown.discard(uid)
    await start_position(uid)

async def start_position(uid):
    state = user_state.get(uid)
    if not state:
        return
    step = state["step"]
    if step > 12:
        await bot.send_message(uid, "Ты прошёл(ла) 12 шагов по методу суперкомпенсации ☀️\nКожа адаптировалась. Теперь можно поддерживать загар в своём ритме.", reply_markup=get_end_keyboard(12))
        return
    pos = state["position"]
    try:
        name = POSITIONS[pos]
        dur = DURATIONS_MIN[step-1][pos]
        msg = await bot.send_message(uid, f"{name} — {format_duration(dur)}\n⏳ Осталось: ...", reply_markup=get_control_keyboard(step))
        state["position"] += 1
        if uid in tasks:
            tasks[uid].cancel()
        tasks[uid] = asyncio.create_task(timer(uid, int(dur * 60), msg))
    except IndexError:
        if uid not in step_completion_shown:
            step_completion_shown.add(uid)
            message = "Шаг завершён. Выбирай ▶️ Продолжить или отдохни ☀️."
            if step <= 2:
                message += "\nЕсли был перерыв — вернись на шаг 1."
            else:
                message += "\nЕсли был перерыв — вернись на 2 шага назад."
            await bot.send_message(uid, message, reply_markup=get_continue_keyboard(step))

async def timer(uid, seconds, msg):
    start = time.monotonic()
    while True:
        elapsed = time.monotonic() - start
        remaining = max(0, int(seconds - elapsed))
        minutes = remaining // 60
        seconds_remain = remaining % 60
        time_text = f"⏳ Осталось: {minutes} мин {seconds_remain} сек" if minutes else f"⏳ Осталось: {seconds_remain} сек"
        new_text = f"{msg.text.splitlines()[0]}\n{time_text}"
        try:
            await bot.edit_message_text(chat_id=uid, message_id=msg.message_id, text=new_text)
        except:
            pass
        if remaining <= 0:
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
    state = user_state.get(uid)
    if state:
        user_state[uid] = {"last_step": state.get("step", 1)}
    else:
        user_state[uid] = {"last_step": 1}
    step = user_state[uid].get("last_step", 1)
    step_completion_shown.discard(uid)
    await bot.send_message(
        uid,
        "Сеанс завершён. Можешь вернуться позже и начать заново ☀️",
        reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(
            KeyboardButton("📋 Вернуться к шагам"),
            KeyboardButton("↩️ Назад на 2 шага (после перерыва)") if step > 2 else KeyboardButton("↩️ Назад на шаг 1 (если был перерыв)")
        )
    )

@dp.message_handler(lambda m: m.text.startswith("↩️"))
async def back(msg: types.Message):
    uid = msg.chat.id
    t = tasks.pop(uid, None)
    if t: t.cancel()
    last = user_state.get(uid, {}).get("last_step", 1)
    step = 1 if last <= 2 else last - 2
    user_state[uid] = {"step": step, "position": 0}
    step_completion_shown.discard(uid)
    await bot.send_message(uid, f"Шаг {step}")
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
    t = tasks.pop(uid, None)
    if t: t.cancel()
    state = user_state.get(uid)
    if not state:
        return
    step = state["step"] + 1
    if step > 12:
        await bot.send_message(uid, "Ты прошёл(ла) 12 шагов по методу суперкомпенсации ☀️\nКожа адаптировалась. Теперь можно поддерживать загар в своём ритме.", reply_markup=get_end_keyboard(12))
        return
    user_state[uid] = {"step": step, "position": 0}
    step_completion_shown.discard(uid)
    await bot.send_message(uid, f"Шаг {step}")
    await start_position(uid)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
