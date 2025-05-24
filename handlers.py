
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from utils import is_subscribed

async def start_handler(message: types.Message):
    if await is_subscribed(message.bot, message.from_user.id):
        from main import get_step_keyboard
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
        keyboard = InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton("✅ Да, я подписан(а)", callback_data="check_sub")
        )
        await message.answer(
            "Бот работает только для подписчиков Telegram-канала SUNXSTYLE.\n"
            "Пожалуйста, подпишись на канал: https://t.me/sunxstyle",
            reply_markup=keyboard
        )

async def info_handler(message: types.Message):
    await message.answer(
        "ℹ️ Инфо\n"
        "Метод суперкомпенсации — это безопасный, пошаговый подход к загару.\n"
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

async def check_sub_callback(callback_query: types.CallbackQuery):
    if await is_subscribed(callback_query.bot, callback_query.from_user.id):
        from main import get_step_keyboard
        await callback_query.message.edit_text(
            "Привет, солнце! ☀️\n"
            "Ты в таймере по методу суперкомпенсации.\n"
            "Кожа адаптируется к солнцу постепенно — и загар становится ровным, глубоким и без ожогов.\n\n"
            "Начинай с шага 1. Даже если уже немного загорел(а), важно пройти путь с начала.\n"
            "Каждый новый день и после перерыва — возвращайся на 2 шага назад.\n\n"
            "Хочешь разобраться подробнее — жми /info. Там всё по делу.",
            reply_markup=get_step_keyboard()
        )
    else:
        await callback_query.answer("Подпишись на канал, чтобы пользоваться ботом", show_alert=True)

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=["start"])
    dp.register_message_handler(info_handler, commands=["info"])
    dp.register_callback_query_handler(check_sub_callback, lambda c: c.data == "check_sub")
