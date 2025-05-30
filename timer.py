
import asyncio
from aiogram import Bot
from state import user_state, tasks, step_completion_shown
from keyboards import get_control_keyboard

# Позиции и длительности по умолчанию (замените на реальные при необходимости)
POSITIONS = ["Лицом вверх", "На животе", "Левый бок", "Правый бок", "В тени"]
DURATIONS = [
    [8, 8, 5, 5, 10],  # пример длительности в минутах для шага 1
    # Добавьте остальные шаги
]

async def start_position(bot: Bot, user_id: int):
    state = user_state.get(user_id)
    if not state:
        return

    step = state["step"]
    position_index = state.get("position", 0)
    durations = DURATIONS[step - 1] if step - 1 < len(DURATIONS) else []
    tasks[user_id] = asyncio.create_task(run_positions(bot, user_id, durations, position_index))

async def run_positions(bot: Bot, user_id: int, durations, start_index=0):
    for i in range(start_index, len(POSITIONS)):
        user_state[user_id]["position"] = i
        minutes = durations[i]
        text = f"{POSITIONS[i]} — {minutes} мин\n⏳ Таймер запущен..."
        await bot.send_message(user_id, text, reply_markup=get_control_keyboard())
        await asyncio.sleep(minutes * 60)  # ожидание таймера
    step_completion_shown.add(user_id)
    await bot.send_message(
        user_id,
        "Шаг завершён. Выбирай ▶️ Продолжить или отдохни ☀️.\nЕсли был перерыв — вернись на 2 шага назад.",
        reply_markup=get_control_keyboard()
    )

async def skip_to_next_position(bot: Bot, user_id: int):
    task = tasks.get(user_id)
    if task:
        task.cancel()
    state = user_state.get(user_id)
    if state:
        state["position"] += 1
        await start_position(bot, user_id)
