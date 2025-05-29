from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

inline_menu = InlineKeyboardMarkup(row_width=1)
inline_menu.add(
    InlineKeyboardButton("▶️ Начать", callback_data="start"),
    InlineKeyboardButton("ℹ️ Инфо", callback_data="info"),
    InlineKeyboardButton("📋 Выбрать шаг", callback_data="choose_step")
)
