from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup
import os
from timer import run_timer
from texts import GREETING, INFO_TEXT
from steps import STEPS
from keyboards import steps_keyboard, get_control_keyboard
from state import user_state, step_completion_shown

bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    await msg.answer(GREETING, reply_markup=steps_keyboard)

@dp.message_handler(commands=["info"])
async def info(msg: types.Message):
    await msg.answer(INFO_TEXT)

@dp.message_handler(lambda msg: msg.text.startswith("Шаг "))
async def handle_step(msg: types.Message):
    chat_id = msg.chat.id
    step_number = int(msg.text.split(" ")[1])
    user_state[chat_id] = {"step": step_number, "position": 0}
    step_completion_shown.discard(chat_id)
    await run_timer(bot, chat_id, step_number)
