from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
menu_keyboard.add(
    KeyboardButton("▶️ Начать"),
    KeyboardButton("ℹ️ Инфо"),
    KeyboardButton("📋 Выбрать шаг")
)
