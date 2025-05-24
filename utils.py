
import aiohttp
import os

CHANNEL_ID = '@sunxstyle'

async def is_subscribed(bot, user_id):
    try:
        chat_member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return chat_member.status in ['member', 'creator', 'administrator']
    except Exception:
        return False
