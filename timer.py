import asyncio
from bot import bot
from keyboards import format_duration

async def timer(uid, total_seconds, message, start_position):
    for remaining in range(total_seconds, 0, -1):
        mins, secs = divmod(remaining, 60)
        time_label = f"{mins} мин {secs:02d} сек" if mins else f"{secs} сек"
        try:
            await bot.edit_message_text(
                text=f"⏳ Осталось: {time_label}",
                chat_id=message.chat.id,
                message_id=message.message_id
            )
        except:
            pass
        await asyncio.sleep(1)

    await start_position(uid)




