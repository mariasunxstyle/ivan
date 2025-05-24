async def is_subscribed(bot, user_id):
    try:
        cm = await bot.get_chat_member('@sunxstyle', user_id)
        return cm.status in ('member', 'administrator', 'creator')
    except:
        return False

# Функция перехода между позициями внутри шага
async def advance_position(chat_id):
    from keyboards import get_post_step_keyboard, get_control_keyboard
    from main import state, positions_by_step, tell_position, bot

    usr = state.get(chat_id)
    if not usr:
        return

    step, pos_index = usr["step"], usr["pos_index"]
    pos_index += 1

    if pos_index >= len(positions_by_step[step]):
        await bot.send_message(chat_id, "Шаг завершён!", reply_markup=get_post_step_keyboard())
        state.pop(chat_id, None)
    else:
        usr["pos_index"] = pos_index
        await tell_position(chat_id, step, pos_index)
