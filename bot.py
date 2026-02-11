import os
import asyncio
import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# 1. Берем ключи из переменных окружения (безопасно)
BOT_TOKEN = os.getenv("BOT_TOKEN")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def get_world_news():
    url = f"https://newsapi.org/v2/top-headlines?category=general&language=en&pageSize=5&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    data = response.json()
    articles = data.get("articles", [])
    news_text = ""
    for article in articles:
        news_text += f"📰 {article['title']}\n{article['url']}\n\n"
    return news_text if news_text else "Жаңалықтар табылмады."

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Сәлем! Әлемдік жаңалықтарды алу үшін /news теріңіз")

@dp.message(Command("news"))
async def news_handler(message: types.Message):
    news = get_world_news()
    await message.answer(news)

async def main():
    # Если вы на Render, порт нужно просто "занять", чтобы сервис не падал
    # Для простого бота на старте используем polling:
    await dp.start_polling(bot)

if __name__ == "__main__":
    # 2. Тот самый отрывок про PORT (важен для деплоя на Render)
    PORT = int(os.environ.get("PORT", 10000))
    asyncio.run(main())
