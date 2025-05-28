
import asyncio
from aiogram.utils.exceptions import MessageNotModified
from bot import bot

async def timer(uid, total_seconds, message, callback, position_name):
    try:
        for remaining in range(total_seconds, 0, -1):
            mins, secs = divmod(remaining, 60)
            time_label = f"{mins} мин {secs:02d} сек" if mins else f"{secs} сек"
            try:
                await bot.edit_message_text(
                    text=f"{position_name} — ⏳ Осталось: {time_label}",
                    chat_id=message.chat.id,
                    message_id=message.message_id,
                    reply_markup=message.reply_markup
                )
            except MessageNotModified:
                pass
            await asyncio.sleep(1)
        await callback(uid)
    except asyncio.CancelledError:
        pass
