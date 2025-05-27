import time
import asyncio
from bot import bot
from state import user_state

async def timer(uid, seconds, msg):
    start = time.monotonic()

    # Отправляем позицию отдельно
    try:
        await bot.send_message(uid, msg.text)
    except Exception as e:
        print("Ошибка отправки позиции:", e)

    while True:
        elapsed = time.monotonic() - start
        remaining = max(0, int(seconds - elapsed))

        minutes = remaining // 60
        seconds_remain = remaining % 60
        time_label = f"{minutes} мин {seconds_remain} сек" if minutes > 0 else f"{seconds_remain} сек"

        try:
            await bot.send_message(uid, f"⏳ Осталось: {time_label}")
        except Exception as e:
            print("Ошибка отправки таймера:", e)

        if remaining <= 0:
            break

        await asyncio.sleep(2)

    if uid in user_state:
        from handlers import start_position
        await start_position(uid)

