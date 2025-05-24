from aiogram import types
from aiogram.dispatcher import Dispatcher
from utils import is_subscribed
from keyboards import get_step_keyboard

async def start_handler(message: types.Message):
    if await is_subscribed(message.bot, message.from_user.id):
        await message.answer(
            "Привет, солнце! ☀️\n"
            "Ты в таймере по методу суперкомпенсации.\n"
            "Кожа адаптируется к солнцу постепенно — и загар получается ровным, глубоким и без ожогов.\n\n"
            "Метод основан на научных принципах: короткие интервалы активируют выработку меланина и гормонов адаптации.\n"
            "Такой подход снижает риск ожогов и делает загар устойчивым.\n\n"
            "Начинай с шага 1 — даже если уже немного загорел(а).\n"
            "Каждый новый день и после перерыва — возвращайся на 2 шага назад.\n\n"
            "Хочешь подробности — жми /info.",
            reply_markup=get_step_keyboard()
        )
    else:
        markup = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("✅ Я подписан(а)", callback_data="check_sub")
        )
        await message.answer("Чтобы пользоваться ботом, нужно быть подписан(а) на канал @sunxstyle.", reply_markup=markup)

async def info_handler(message: types.Message):
    await message.answer(
        "Метод суперкомпенсации — научно обоснованный способ безопасного загара.\n"
        "Ты проходишь 12 шагов — каждый с таймингом и сменой позиций.\n\n"
        "Как использовать:\n"
        "1. Начни с шага 1\n"
        "2. Включи таймер и следуй позициям\n"
        "3. Каждый новый день и после любого перерыва — возвращайся на 2 шага назад\n"
        "4. После завершения всех 12 шагов — можешь поддерживать загар в комфортном ритме\n\n"
        "Рекомендуем загорать с 7:00 до 11:00 и после 17:00 — в это время солнце мягкое, и при отсутствии противопоказаний можно загорать без SPF.\n"
        "С 11:00 до 17:00 — солнце более агрессивное. Если остаёшься на улице — надевай одежду или используй SPF.\n\n"
        "Если есть вопросы — пиши: @sunxbeach_director"
    )

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=["start"])
    dp.register_message_handler(info_handler, commands=["info"])
