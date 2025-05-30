import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

from keyboards import steps_keyboard, get_control_keyboard
from state import user_state, tasks, step_completion_shown
from texts import GREETING, INFO_TEXT
from timer import start_position

load_dotenv()
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
    try:
        step = int(msg.text.split()[1])
    except:
        await msg.answer("Неверный формат шага. Попробуй снова.")
        return
    user_state[msg.chat.id] = {"step": step, "position": 0}
    step_completion_shown.discard(msg.chat.id)
    await start_position(bot, msg.chat.id)

@dp.message_handler(lambda m: m.text == "📋 Вернуться к шагам")
async def back_to_steps(msg: types.Message):
    await msg.answer("Выбери шаг:", reply_markup=steps_keyboard)

@dp.message_handler(lambda m: m.text == "↩️ Назад на 2 шага")
@dp.message_handler(lambda m: m.text == "↩️ Назад на 2 шага (если был перерыв)")
async def step_back(msg: types.Message):
    state = user_state.get(msg.chat.id)
    if state:
        current_step = state.get("step", 1)
        new_step = max(1, current_step - 2)
        user_state[msg.chat.id] = {"step": new_step, "position": 0}
        step_completion_shown.discard(msg.chat.id)
        await msg.answer(f"Возврат на шаг {new_step}.")
        await start_position(bot, msg.chat.id)

@dp.message_handler(lambda m: m.text == "⛔ Завершить")
async def end_session(msg: types.Message):
    tasks.pop(msg.chat.id, None)
    step_completion_shown.discard(msg.chat.id)
    await msg.answer("Сеанс завершён. Можешь вернуться позже и начать заново ☀️",
                     reply_markup=get_control_keyboard())

@dp.message_handler(lambda m: m.text == "⏭️ Пропустить")
async def skip_position(msg: types.Message):
    from timer import skip_to_next_position
    await skip_to_next_position(bot, msg.chat.id)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
