
async def is_subscribed(bot, user_id):
    try:
        cm = await bot.get_chat_member('@sunxstyle', user_id)
        return cm.status in ('member', 'administrator', 'creator')
    except:
        return False
