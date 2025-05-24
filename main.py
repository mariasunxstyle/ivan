
import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

from keyboards import get_step_keyboard, get_control_keyboard
from utils import is_subscribed
from steps import steps, positions_by_step

API_TOKEN = os.getenv("TOKEN")
CHANNEL = "@sunxstyle"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# храним прогресс пользователя
state = {}  # user_id: {"step": int, "pos_index": int}

WELCOME = (
    "Привет, солнце! ☀️\n"
    "Ты в таймере по методу суперкомпенсации.\n"
    "Кожа адаптируется к солнцу постепенно — и загар становится ровным, глубоким и без ожогов.\n\n"
    "Начинай с шага 1. Даже если уже немного загорел(а), важно пройти путь с начала.\n"
    "Каждый новый день и после перерыва — возвращайся на 2 шага назад.\n\n"
    "Хочешь разобраться подробнее — жми /info. Там всё по делу."
)

INFO = (
    "ℹ️ Метод суперкомпенсации — это безопасный, пошаговый подход к загару.\n"
    "Он помогает коже адаптироваться к солнцу, снижая риск ожогов и пятен.\n\n"
    "Рекомендуем загорать с 7:00 до 11:00 и после 17:00 — в это время солнце мягкое,\n"
    "и при отсутствии противопоказаний можно загорать без SPF.\n"
    "Так кожа включает свою естественную защиту: вырабатывается меланин и гормоны адаптации.\n\n"
    "С 11:00 до 17:00 — солнце более агрессивное. Если остаёшься на улице —\n"
    "надевай одежду, головной убор или используй SPF.\n\n"
    "Каждый новый день и после перерыва — возвращайся на 2 шага назад.\n"
    "Это нужно, чтобы кожа не перегружалась и постепенно усиливала защиту.\n\n"
    "Если есть вопросы — пиши: @sunxbeach_director"
)

# ----- helpers -------------------------------------------------
def human_time(minutes: int) -> str:
    h, m = divmod(minutes, 60)
    return f"{h} ч {m} мин" if h else f"{m} мин"

async def tell_position(chat_id: int, step: int, pos_index: int):
    name, mins = positions_by_step[step][pos_index]
    await bot.send_message(chat_id, f"{name} — {human_time(mins)}")

async def advance_position(chat_id: int):
    usr = state.get(chat_id)
    if not usr:
        return
    step, pos_index = usr["step"], usr["pos_index"]
    pos_index += 1
    if pos_index >= len(positions_by_step[step]):
        await bot.send_message(chat_id, "Шаг завершён!", reply_markup=get_step_keyboard())
        del state[chat_id]
    else:
        usr["pos_index"] = pos_index
        await tell_position(chat_id, step, pos_index)

# ----- handlers ------------------------------------------------
@dp.message_handler(commands=["start"])
async def cmd_start(m: types.Message):
    if await is_subscribed(bot, m.from_user.id):
        await m.answer(WELCOME, reply_markup=get_step_keyboard())
    else:
        kb = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("✅ Я подписан(а)", callback_data="check_sub"))
        await m.answer("Чтобы пользоваться ботом, нужно быть подписан(а) на канал @sunxstyle.", reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data == "check_sub")
async def cb_check_sub(call: types.CallbackQuery):
    if await is_subscribed(bot, call.from_user.id):
        await call.message.edit_text(WELCOME, reply_markup=get_step_keyboard())
    else:
        await call.answer("Пока не вижу подписки...", show_alert=True)

@dp.message_handler(commands=["info"])
async def cmd_info(m: types.Message):
    await m.answer(INFO)

@dp.message_handler(lambda m: m.text and m.text.startswith("Шаг"))
async def select_step(m: types.Message):
    step_num = int(m.text.split()[1])
    state[m.from_user.id] = {"step": step_num, "pos_index": 0}
    await tell_position(m.chat.id, step_num, 0)
    await m.answer(" ", reply_markup=get_control_keyboard())

@dp.message_handler(lambda m: m.text == "⏭️ Пропустить")
async def skip(m: types.Message):
    await advance_position(m.chat.id)

@dp.message_handler(lambda m: m.text == "⛔ Завершить")
async def stop(m: types.Message):
    state.pop(m.chat.id, None)
    await m.answer("Сеанс завершён. Можешь вернуться позже и начать заново ☀️", reply_markup=get_step_keyboard())

@dp.message_handler(lambda m: m.text.startswith("↩️ Назад"))
async def back_two(m: types.Message):
    usr = state.get(m.chat.id, {"step": 1})
    new_step = max(1, usr["step"] - 2)
    state[m.chat.id] = {"step": new_step, "pos_index": 0}
    await tell_position(m.chat.id, new_step, 0)

@dp.message_handler(lambda m: m.text == "📋 Вернуться к шагам")
async def to_menu(m: types.Message):
    state.pop(m.chat.id, None)
    await m.answer("Выбери шаг:", reply_markup=get_step_keyboard())

# background position timer
async def pos_timer():
    while True:
        await asyncio.sleep(60)  # tick every minute
        for chat_id in list(state.keys()):
            usr = state[chat_id]
            step = usr["step"]
            name, mins = positions_by_step[step][usr["pos_index"]]
            usr.setdefault("elapsed", 0)
            usr["elapsed"] += 1
            if usr["elapsed"] >= mins:
                usr["elapsed"] = 0
                await advance_position(chat_id)

if __name__ == "__main__":
    dp.loop.create_task(pos_timer())
    executor.start_polling(dp, skip_updates=True)
