import time
import asyncio
from bot import bot
from state import user_state
from handlers import start_position
from keyboards import POSITIONS

async def timer(uid, total_seconds, msg):
    start_time = time.monotonic()
    last_text = ""

    while True:
        elapsed = int(time.monotonic() - start_time)
        remaining = max(0, total_seconds - elapsed)

        minutes = remaining // 60
        seconds = remaining % 60

        text = f"⏳ Осталось: {minutes} мин {seconds} сек" if minutes > 0 else f"⏳ Осталось: {seconds} сек"

        if text != last_text:
            try:
                await bot.edit_message_text(
                    chat_id=uid,
                    message_id=msg.message_id,
                    text=text,
                    reply_markup=msg.reply_markup
                )
                last_text = text
            except Exception:
                break

        if remaining <= 0:
            break

        await asyncio.sleep(1)

    # Переход к следующей позиции
    if uid in user_state:
        await start_position(uid)





