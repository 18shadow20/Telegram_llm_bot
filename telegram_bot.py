from aiogram import Bot, Dispatcher, types
from llm import answer_llm
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

bot = Bot(os.getenv("TELEGRAM_TOKEN"))
dp = Dispatcher()

@dp.message()
async def message(message:types.Message):
    user_text = message.text
    answer = answer_llm(user_text)
    await message.answer(answer)

asyncio.run(dp.start_polling(bot))