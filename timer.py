import time
import asyncio
from bot import bot
from state import user_state

async def timer(uid, seconds, msg):
    start = time.monotonic()

    # Отправляем позицию и сохраняем сообщение
    try:
        sent = await bot.send_message(uid, msg.text)
    except Exception as e:
        print("Ошибка отправки позиции:", e)
        return

    position_text = msg.text  # сохраняем текст позиции один раз
    last_state = ""

    while True:
        elapsed = time.monotonic() - start
        remaining = max(0, int(seconds - elapsed))

        minutes = remaining // 60
        seconds_remain = remaining % 60
        time_label = f"{minutes} мин {seconds_remain} сек" if minutes > 0 else f"{seconds_remain} сек"

        new_text = f"{position_text}\n⏳ Осталось: {time_label}"

        if new_text != last_state:
            try:
                await bot.edit_message_text(
                    chat_id=uid,
                    message_id=sent.message_id,
                    text=new_text
                )
            except Exception as e:
                print("Ошибка редактирования таймера:", e)
            last_state = new_text

        if remaining <= 0:
            break

        await asyncio.sleep(2)

    if uid in user_state:
        from handlers import start_position
        await start_position(uid)

