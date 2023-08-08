import asyncio
import os
from datetime import datetime

import pytz
import requests
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

load_dotenv()
bot = Bot(token=os.getenv("API_TOKEN"))
dp = Dispatcher(bot)
chat_ids = []


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer(f"Hi {message.from_user.first_name}\nI am a bot which send weather every day\nWrite your city")
    chat_ids.append(message.from_user.id)


async def schedule_weather():
    while True:
        tz = pytz.timezone("Asia/Tashkent")
        now = datetime.now(tz=tz)
        if now.hour in [7, 12, 16, 20] and now.minute == 30:
            page = requests.get(f'https://wttr.in/{os.getenv("CITY")}?format=3')
            for chat_id in chat_ids:
                await bot.send_message(chat_id, page.content.decode("utf-8"))
            await asyncio.sleep(3600)

if __name__ == "__main__":
    executor.start_polling(dp)
    asyncio.ensure_future(schedule_weather())
