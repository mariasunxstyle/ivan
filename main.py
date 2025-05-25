import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from steps import steps
import os

API_TOKEN = os.getenv("TOKEN") or "вставь_сюда_свой_токен"
CHANNEL_USERNAME = "@sunxstyle"

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class SessionState(StatesGroup):
    tanning = State()

def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    buttons = [KeyboardButton(f"Шаг {s['step']} — {s['duration_min']} мин") for s in steps]
    keyboard.add(*buttons)
    keyboard.add(KeyboardButton("ℹ️ Инфо"))
    return keyboard

def get_control_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("⏭️ Пропустить"))
    keyboard.add(KeyboardButton("⛔ Завершить"))
    keyboard.add(KeyboardButton("↩️ Назад на 2 шага"))
    keyboard.add(KeyboardButton("📋 Вернуться к шагам"))
    return keyboard

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    chat_member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
    if chat_member.status not in ["member", "creator", "administrator"]:
        await message.answer("Подпишись на канал @sunxstyle, чтобы пользоваться ботом")
        return

    text = (
        "Привет, солнце! ☀️\n"
        "Ты в таймере по методу суперкомпенсации.\n"
        "Кожа адаптируется к солнцу постепенно — и загар получается ровным, глубоким и без ожогов.\n\n"
        "Метод основан на научных принципах: короткие интервалы активируют выработку меланина и гормонов адаптации.\n"
        "Такой подход снижает риск ожогов и делает загар устойчивым.\n\n"
        "Начинай с шага 1 — даже если уже немного загорел(а).\n"
        "Каждый новый день и после перерыва — возвращайся на 2 шага назад.\n\n"
        "Хочешь подробности — жми /info."
    )
    await message.answer(text, reply_markup=get_main_keyboard())

@dp.message_handler(lambda message: message.text.startswith("Шаг "))
async def handle_step(message: types.Message, state: FSMContext):
    step_num = int(message.text.split()[1])
    step = next(s for s in steps if s['step'] == step_num)
    await message.answer(f"Шаг {step_num} запущен. Готовься ☀️")
    await state.update_data(step=step_num, position_index=0)
    await SessionState.tanning.set()
    await run_positions(message.chat.id, step_num, state)

async def run_positions(chat_id, step_num, state: FSMContext):
    step = next(s for s in steps if s['step'] == step_num)
    data = await state.get_data()
    position_index = data.get("position_index", 0)

    if position_index >= len(step['positions']):
        await bot.send_message(chat_id, f"Шаг {step_num} завершён! ☀️\nВыбирай следующий шаг или отдохни.", reply_markup=get_main_keyboard())
        await state.finish()
        return

    pos = step['positions'][position_index]
    duration = int(pos['minutes'] * 60)
    await bot.send_message(chat_id, f"{pos['name']} — {pos['minutes']} мин", reply_markup=get_control_keyboard())
    await asyncio.sleep(duration)

    await state.update_data(position_index=position_index + 1)
    await run_positions(chat_id, step_num, state)

@dp.message_handler(lambda message: message.text in ["⏭️ Пропустить", "⛔ Завершить", "↩️ Назад на 2 шага", "📋 Вернуться к шагам"])
async def handle_controls(message: types.Message, state: FSMContext):
    data = await state.get_data()
    step_num = data.get("step")
    position_index = data.get("position_index", 0)

    if message.text == "⏭️ Пропустить":
        await state.update_data(position_index=position_index + 1)
        await run_positions(message.chat.id, step_num, state)

    elif message.text == "⛔ Завершить":
        await state.finish()
        await message.answer("Сеанс завершён. Можешь вернуться позже и начать заново ☀️", reply_markup=get_main_keyboard())

    elif message.text == "↩️ Назад на 2 шага":
        target_step = max(1, step_num - 2)
        await message.answer(f"Ты вернулся(ась) к шагу {target_step} ☀️", reply_markup=get_main_keyboard())
        await state.finish()

    elif message.text == "📋 Вернуться к шагам":
        await message.answer("📋 Выбери шаг", reply_markup=get_main_keyboard())
        await state.finish()

@dp.message_handler(lambda message: message.text == "ℹ️ Инфо")
async def show_info(message: types.Message):
    info = (
        "ℹ️ Инфо\n"
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
    await message.answer(info)

if __name__ == '__main__':
    executor.start_polling(dp)
