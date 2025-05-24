
# coding: utf-8

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import os
import logging

from steps import steps
from utils import is_subscribed, get_time_label
from keyboards import get_step_keyboard, get_control_keyboard

API_TOKEN = os.getenv("TOKEN")
CHANNEL_USERNAME = "@sunxstyle"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

user_states = {}

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    if await is_subscribed(bot, message.from_user.id):
        await message.answer(
            "Привет, солнце! ☀️\n"
            "Ты в таймере по методу суперкомпенсации.\n"
            "Кожа адаптируется к солнцу постепенно — и загар становится ровным, глубоким и без ожогов.\n\n"
            "Начинай с шага 1. Даже если уже немного загорел(а), важно пройти путь с начала.\n"
            "Каждый новый день и после перерыва — возвращайся на 2 шага назад.\n\n"
            "Хочешь разобраться подробнее — жми /info. Там всё по делу.",
            reply_markup=get_step_keyboard()
        )
    else:
        kb = InlineKeyboardMarkup().add(InlineKeyboardButton("✅ Я подписан(а)", callback_data="check_sub"))
        await message.answer("Чтобы пользоваться ботом, нужно быть подписан(а) на канал @sunxstyle.", reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data == "check_sub")
async def check_sub(call: types.CallbackQuery):
    if await is_subscribed(bot, call.from_user.id):
        await call.message.edit_text(
            "Привет, солнце! ☀️\n"
            "Ты в таймере по методу суперкомпенсации.\n"
            "Кожа адаптируется к солнцу постепенно — и загар становится ровным, глубоким и без ожогов.\n\n"
            "Начинай с шага 1. Даже если уже немного загорел(а), важно пройти путь с начала.\n"
            "Каждый новый день и после перерыва — возвращайся на 2 шага назад.\n\n"
            "Хочешь разобраться подробнее — жми /info. Там всё по делу.",
            reply_markup=get_step_keyboard()
        )
    else:
        await call.answer("Пока не вижу подписки...", show_alert=True)

@dp.message_handler(commands=['info'])
async def info_cmd(message: types.Message):
    await message.answer(
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

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
