async def start_position(uid):
    state = user_state.get(uid)
    if not state:
        return
    step = state["step"]
    pos = state["position"]
    if step > 12:
        await bot.send_message(uid, "Ты прошёл(ла) 12 шагов по методу суперкомпенсации ☀️\nКожа адаптировалась. Теперь можно поддерживать загар в своём ритме.", reply_markup=get_end_keyboard(step))
        return
    try:
        name = POSITIONS[pos]
        dur = DURATIONS_MIN[step-1][pos]
        msg = await bot.send_message(uid, f"{name} — {format_duration(dur)}\n⏳ Осталось: ...", reply_markup=get_control_keyboard(step))
        state["position"] += 1
        if uid in tasks:
            tasks[uid].cancel()
        tasks[uid] = asyncio.create_task(timer(uid, int(dur * 60), msg))
    except IndexError:
        if uid not in step_completion_shown:
            step_completion_shown.add(uid)
            message = "Шаг завершён. Выбирай ▶️ Продолжить или отдохни ☀️."
            if step <= 2:
                message += "\nЕсли был перерыв — вернись на шаг 1."
            else:
                message += "\nЕсли был перерыв — вернись на 2 шага назад."
            await bot.send_message(uid, message, reply_markup=get_continue_keyboard(step))

async def timer(uid, seconds, msg):
    start = time.monotonic()
    last_text = ""
    while True:
        elapsed = time.monotonic() - start
        remaining = max(0, int(seconds - elapsed))
        if remaining <= 0:
            break
        minutes = remaining // 60
        seconds_remain = remaining % 60
        time_str = f"⏳ Осталось: {minutes:02d}:{seconds_remain:02d}"
        new_text = f"{msg.text.splitlines()[0]}\n{time_str}"
        if new_text != last_text:
            try:
                await bot.edit_message_text(new_text, chat_id=uid, message_id=msg.message_id, reply_markup=get_control_keyboard(user_state[uid]['step']))
                last_text = new_text
            except:
                pass
        await asyncio.sleep(1)
    if uid in user_state:
        await start_position(uid)

@dp.message_handler(lambda m: m.text == "⏭️ Пропустить")
async def skip(msg: types.Message):
    uid = msg.chat.id
    t = tasks.pop(uid, None)
    if t: t.cancel()
    await start_position(uid)

@dp.message_handler(lambda m: m.text == "⛔ Завершить")
async def end(msg: types.Message):
    uid = msg.chat.id
    t = tasks.pop(uid, None)
    if t: t.cancel()
    state = user_state.get(uid)
    if state:
        user_state[uid] = {"last_step": state.get("step", 1)}
    else:
        user_state[uid] = {"last_step": 1}
    step = user_state[uid].get("last_step", 1)
    step_completion_shown.discard(uid)
    await bot.send_message(
        uid,
        "Сеанс завершён. Можешь вернуться позже и начать заново ☀️",
        reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(
            KeyboardButton("📋 Вернуться к шагам"),
            KeyboardButton("↩️ Назад на 2 шага (после перерыва)") if step > 2 else KeyboardButton("↩️ Назад на шаг 1 (если был перерыв)")
        )
    )
