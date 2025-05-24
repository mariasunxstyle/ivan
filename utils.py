
import aiohttp

async def is_subscribed(bot, user_id):
    try:
        chat_member = await bot.get_chat_member('@sunxstyle', user_id)
        return chat_member.status in ['member', 'administrator', 'creator']
    except:
        return False

def get_time_label(mins):
    h, m = divmod(mins, 60)
    return f"{h} ч {m} мин" if h else f"{m} мин"
