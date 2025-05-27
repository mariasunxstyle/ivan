from aiogram import types
from bot import bot, dp
import asyncio, time

from texts import GREETING, INFO_TEXT
from keyboards import POSITIONS, DURATIONS_MIN, format_duration
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from state import user_state, tasks, step_completion_shown

# === Генерация клавиатур ===

steps_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
step_buttons = []
for i, row in enumerate(DURATIONS_MIN):
    total = sum(row)
    h = int(total // 60)
    m = int(total % 60)
    label = f"Шаг {i + 1} ({f'{h} ч ' if h else ''}{m} мин)"
    step_buttons.append(KeyboardButton(label))
for i in range(0, len(step_buttons), 4):
    steps_keyboard.add(*step_buttons[i:i + 4])
steps_keyboard.add(KeyboardButton("ℹ️ Инфо"))

def get_control_keyboard(step):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("⏭️ Пропустить"))
    kb.add(KeyboardButton("⛔ Завершить"))
    kb.add(KeyboardButton("↩️ Назад на шаг 1 (если был перерыв)") if step <= 2 else KeyboardButton("↩️ Назад на 2 шага (после перерыва)"))
    kb.add(KeyboardButton("📋 Вернуться к шагам"))
    return kb

def get_continue_keyboard(step):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("▶️ Продолжить"))
    kb.add(KeyboardButton("📋 Вернуться к шагам"))
    kb.add(KeyboardButton("↩️ Назад на шаг 1 (если был перерыв)") if step <= 2 else KeyboardButton("↩️ Назад на 2 шага (после перерыва)"))
    kb.add(KeyboardButton("⛔ Завершить"))
    return kb

control_keyboard_full = ReplyKeyboardMarkup(resize_keyboard=True)
control_keyboard_full.add(KeyboardButton("📋 Вернуться к шагам"))
control_keyboard_full.add(KeyboardButton("↩️ Назад на 2 шага (после перерыва)"))
control_keyboard_full.add(KeyboardButton("⛔ Завершить"))

end_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
end_keyboard.add(
    KeyboardButton("📋 Вернуться к шагам"),
    KeyboardButton("↩️ Назад на 2 шага (после перерыва)")
)

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
Кожа адаптировалась. Теперь можно поддерживать загар в своём ритме.", reply_markup=control_keyboard_full)
        return
    try:
        name = POSITIONS[pos]
        dur = DURATIONS_MIN[step-1][pos]
        message = await bot.send_message(uid, f"{name} — {format_duration(dur)}
⏳ Таймер запущен...")
        state["position"] += 1
        tasks[uid] = asyncio.create_task(timer(uid, int(dur * 60), message))
    except IndexError:
        if step == 12:
            await bot.send_message(uid, "Ты прошёл(ла) 12 шагов по методу суперкомпенсации ☀️
Кожа адаптировалась. Теперь можно поддерживать загар в своём ритме.", reply_markup=control_keyboard_full)
        elif uid not in step_completion_shown:
            step_completion_shown.add(uid)
            message = "Шаг завершён. Выбирай ▶️ Продолжить или отдохни ☀️."
            message += "
Если был перерыв — вернись на шаг 1." if step <= 2 else "
Если был перерыв — вернись на 2 шага назад."
            await bot.send_message(uid, message, reply_markup=get_continue_keyboard(step))

async def timer(uid, seconds, msg):
    start = time.monotonic()
    bar_states = ["☀️🌑🌑🌑🌑🌑🌑🌑🌑🌑", "☀️☀️🌑🌑🌑🌑🌑🌑🌑🌑", "☀️☀️☀️🌑🌑🌑🌑🌑🌑🌑",
        "☀️☀️☀️☀️🌑🌑🌑🌑🌑🌑", "☀️☀️☀️☀️☀️🌑🌑🌑🌑🌑", "☀️☀️☀️☀️☀️☀️🌑🌑🌑🌑",
        "☀️☀️☀️☀️☀️☀️☀️🌑🌑🌑", "☀️☀️☀️☀️☀️☀️☀️☀️🌑🌑",
        "☀️☀️☀️☀️☀️☀️☀️☀️☀️🌑", "☀️☀️☀️☀️☀️☀️☀️☀️☀️☀️"]
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
        text = f"⏳ Осталось: {time_label}
{bar}"
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
