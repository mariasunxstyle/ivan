# SUNXSTYLE Bot (модульная структура)

Telegram-бот для загара по методу суперкомпенсации ☀️

## Запуск

Создай `.env` с переменной `TOKEN=<твой_токен>`, установи зависимости:

```bash
pip install -r requirements.txt
python main.py
```

## Структура

- `main.py` — запуск и логика
- `keyboards.py` — клавиатуры
- `texts.py` — приветствие и инфо
- `state.py` — шаги и позиции
- `timer.py` — таймер с визуальной шкалой