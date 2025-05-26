from aiogram import Bot, Dispatcher, types, executor
import logging
import os

API_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "123456789"))  # Заменить на свой ID

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

USERS_FILE = "users.txt"

def save_user(user_id):
    try:
        with open(USERS_FILE, "r") as f:
            users = set(f.read().splitlines())
    except FileNotFoundError:
        users = set()
    users.add(str(user_id))
    with open(USERS_FILE, "w") as f:
        f.write("\n".join(users))

def get_user_count():
    try:
        with open(USERS_FILE, "r") as f:
            return len(set(f.read().splitlines()))
    except FileNotFoundError:
        return 0

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    save_user(user_id)
    await message.answer(
        "Привет, солнце! ☀️\n"
        "Ты в таймере по методу суперкомпенсации.\n\n"
        "Загар получается ровный, без ожогов — если следовать шагам: "
        "'перевернись, отдохни, в тень'.\n\n"
        "Начинай с шага 1 — или выбери любой:"
    )

@dp.message_handler(commands=['stats'])
async def stats_handler(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        count = get_user_count()
        await message.reply(f"👥 Пользователей всего: {count}")
    else:
        await message.reply("⛔ Доступ запрещён.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)