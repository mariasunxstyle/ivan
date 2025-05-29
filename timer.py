# Обновлённый run_timer с разделением сообщений и анимацией
import asyncio
import time

bar_states = [
    "☀️🌑🌑🌑🌑🌑🌑🌑🌑🌑", "☀️☀️🌑🌑🌑🌑🌑🌑🌑🌑", "☀️☀️☀️🌑🌑🌑🌑🌑🌑🌑",
    "☀️☀️☀️☀️🌑🌑🌑🌑🌑🌑", "☀️☀️☀️☀️☀️🌑🌑🌑🌑🌑", "☀️☀️☀️☀️☀️☀️🌑🌑🌑🌑",
    "☀️☀️☀️☀️☀️☀️☀️🌑🌑🌑", "☀️☀️☀️☀️☀️☀️☀️☀️🌑🌑",
    "☀️☀️☀️☀️☀️☀️☀️☀️☀️🌑", "☀️☀️☀️☀️☀️☀️☀️☀️☀️☀️"
]

async def run_timer(bot, uid, seconds, user_state, start_position, step):
    start = time.monotonic()
    msg = await bot.send_message(uid, "⏳ Таймер запущен...")
    while True:
        elapsed = time.monotonic() - start
        remaining = int(seconds - elapsed)
        if remaining < 0:
            break

        bar_index = min(int((elapsed / seconds) * 10), 9)
        bar = bar_states[bar_index]
        mins = remaining // 60
        secs = remaining % 60
        text = f"⏳ Осталось: {mins} мин {secs} сек\n{bar}"

        try:
            await bot.edit_message_text(
                chat_id=uid,
                message_id=msg.message_id,
                text=text
            )
        except Exception as e:
            print("[timer] Ошибка редактирования:", e)

        await asyncio.sleep(2)

    if uid in user_state:
        await start_position(uid)
