import asyncio
import time
from steps import format_duration

user_state = {}
tasks = {}
step_completion_shown = set()

async def run_timer(uid, seconds, msg, bot):
    start = time.monotonic()
    bar_states = [
        "☀️🌑🌑🌑🌑🌑🌑🌑🌑🌑", "☀️☀️🌑🌑🌑🌑🌑🌑🌑🌑", "☀️☀️☀️🌑🌑🌑🌑🌑🌑🌑",
        "☀️☀️☀️☀️🌑🌑🌑🌑🌑🌑", "☀️☀️☀️☀️☀️🌑🌑🌑🌑🌑", "☀️☀️☀️☀️☀️☀️🌑🌑🌑🌑",
        "☀️☀️☀️☀️☀️☀️☀️🌑🌑🌑", "☀️☀️☀️☀️☀️☀️☀️☀️🌑🌑",
        "☀️☀️☀️☀️☀️☀️☀️☀️☀️🌑", "☀️☀️☀️☀️☀️☀️☀️☀️☀️☀️"
    ]
    last_state = ""
    while True:
        elapsed = time.monotonic() - start
        remaining = max(0, int(seconds - elapsed))
        percent_done = min(elapsed / seconds, 1.0)
        bar_index = min(int(percent_done * 10), 9)

        bar = bar_states[bar_index]
        minutes = remaining // 60
        seconds_remain = remaining % 60
        time_label = f"{minutes} мин {seconds_remain} сек" if minutes > 0 else f"{seconds_remain} сек"
        text = f"⏳ Осталось: {time_label}\n{bar}"

        if text != last_state:
            try:
                await bot.edit_message_text(text=msg.text.split("\n")[0] + "\n" + text, chat_id=uid, message_id=msg.message_id)
            except:
                pass
            last_state = text

        
    if uid in user_state:
        from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
        from keyboards import steps_keyboard

        step = user_state[uid]["step"]
        if step <= 2:
            back_button = ReplyKeyboardMarkup(resize_keyboard=True)
            back_button.add(KeyboardButton("↩️ Назад на шаг 1 (если был перерыв)"))
            back_button.add(KeyboardButton("📋 Вернуться к шагам"))
            await bot.send_message(uid, "Шаг завершён ☀️
Можешь вернуться позже и начать заново.", reply_markup=back_button)
        else:
            await bot.send_message(uid, "Шаг завершён ☀️
Можешь вернуться позже и начать заново.", reply_markup=steps_keyboard)
        step_completion_shown.add(uid)

