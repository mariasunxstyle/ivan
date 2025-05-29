import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from dotenv import load_dotenv
from texts import GREETING, INFO_TEXT
from keyboards import steps_keyboard, get_control_keyboard
from state import user_state
from timer import run_timer

load_dotenv()
API_TOKEN = os.getenv("TOKEN")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def send_welcome(msg: types.Message):
    user_state[msg.from_user.id] = {"step": None}
    await msg.answer(GREETING, reply_markup=steps_keyboard())

@dp.message_handler(commands=["info"])
async def send_info(msg: types.Message):
    await msg.answer(INFO_TEXT)

@dp.message_handler(lambda msg: msg.text.startswith("Шаг"))
async def start_step(msg: types.Message):
    try:
        step_num = int(msg.text.split()[1])
        user_state[msg.from_user.id] = {"step": step_num}
        await run_timer(bot, msg.chat.id, step_num)
    except Exception as e:
        await msg.answer("Ошибка при запуске шага.")

@dp.message_handler(lambda msg: msg.text == "📋 Вернуться к шагам")
async def return_to_steps(msg: types.Message):
    await msg.answer("Выбери шаг:", reply_markup=steps_keyboard())

@dp.message_handler(lambda msg: msg.text == "⛔ Завершить")
async def cancel_session(msg: types.Message):
    uid = msg.from_user.id
    user_state[uid] = {"step": None}
    await msg.answer("Сеанс завершён. Можешь вернуться позже и начать заново ☀️", reply_markup=steps_keyboard())

@dp.message_handler(lambda msg: msg.text == "↩️ Назад на 2 шага")
async def step_back(msg: types.Message):
    uid = msg.from_user.id
    step = user_state.get(uid, {}).get("step", 1)
    new_step = max(1, step - 2)
    user_state[uid]["step"] = new_step
    await msg.answer(f"Возвращаемся на шаг {new_step}", reply_markup=steps_keyboard())

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
