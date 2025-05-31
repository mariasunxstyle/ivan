import time
import asyncio
from aiogram import Bot

async def run_timer(bot: Bot, uid: int, duration_sec: int, message, on_complete=None):
    start = time.monotonic()
    bar_states = [
        "☀️🌑🌑🌑🌑🌑🌑🌑🌑🌑", "☀️☀️🌑🌑🌑🌑🌑🌑🌑🌑", "☀️☀️☀️🌑🌑🌑🌑🌑🌑🌑",
        "☀️☀️☀️☀️🌑🌑🌑🌑🌑🌑", "☀️☀️☀️☀️☀️🌑🌑🌑🌑🌑", "☀️☀️☀️☀️☀️☀️🌑🌑🌑🌑",
        "☀️☀️☀️☀️☀️☀️☀️🌑🌑🌑", "☀️☀️☀️☀️☀️☀️☀️☀️🌑🌑",
        "☀️☀️☀️☀️☀️☀️☀️☀️☀️🌑", "☀️☀️☀️☀️☀️☀️☀️☀️☀️☀️"
    ]
    last = ""

    while True:
        elapsed = time.monotonic() - start
        remaining = max(0, int(duration_sec - elapsed))
        percent_done = min(elapsed / duration_sec, 1.0)
        bar_index = min(int(percent_done * 10), 9)

        bar = bar_states[bar_index]
        minutes = remaining // 60
        seconds_remain = remaining % 60
        time_label = f"{minutes} мин {seconds_remain} сек" if minutes > 0 else f"{seconds_remain} сек"
        text = f"⏳ Осталось: {time_label}\n{bar}"

        if text != last:
            try:
                await bot.edit_message_text(
                    text=message.text.split('\n')[0] + '\n' + text,
                    chat_id=uid,
                    message_id=message.message_id
                )
            except:
                pass
            last = text

        if remaining <= 0:
            break
        await asyncio.sleep(2)

    if on_complete:
        await on_complete()