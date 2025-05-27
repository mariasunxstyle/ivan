import time
import asyncio
from bot import bot
from state import user_state

async def timer(uid, seconds, msg):
    start = time.monotonic()
    last_state = ""

    while True:
        elapsed = time.monotonic() - start
        remaining = max(0, int(seconds - elapsed))

        minutes = remaining // 60
        seconds_remain = remaining % 60
        time_label = f"{minutes} мин {seconds_remain} сек" if minutes > 0 else f"{seconds_remain} сек"

        new_text = f"⏳ Осталось: {time_label}"  # Без анимации

        if new_text != last_state:
            try:
                await bot.edit_message_text(
                    chat_id=uid,
                    message_id=msg.message_id,
                    text=new_text,
                    reply_markup=msg.reply_markup
                )
            except Exception as e:
                print("Ошибка редактирования:", e)
            last_state = new_text

        if remaining <= 0:
            break

        await asyncio.sleep(2)

    if uid in user_state:
        from handlers import start_position
        await start_position(uid)
