# Telegram LLM Bot

Бот для ответов на вопросы о видео из базы данных с использованием LLM.

## Как запустить

1. Клонируем репозиторий:
```bash
git clone https://github.com/18shadow20/Telegram_llm_bot.git
cd Telegram_llm_bot 
```
2. Создаем виртуальное окружение и устанавливаем зависимости:
```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

3. Настроить .env:
```bash
TELEGRAM_TOKEN=your_telegram_bot_token
GEMINI_API_KEY=your_llm_api_key
DATABASE_URL=postgresql://user:pass@host/dbname
```

4. Загрузить JSON с видео json_loader:


5. Запустить бота:
```bash
python telegram_bot.py
```

telegram_bot.py — точка входа, обработка сообщений Telegram.

utils.py — функции для подсчета видео, просмотров, лайков и др.

database.py — модели SQLAlchemy для Videos и VideoSnapshots.

llm.py — настройка LLM

json_loader — загрузить json в БД

Есди LLM не работает скорее всего нужен VPN

















