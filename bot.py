import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from config import BOT_TOKEN
from middleware.logger import LoggingMiddleware
from db.connection import init_db
from handlers import settings, basic, weather, universal
from utils.default_commands import set_default_commands


bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()
dp.message.middleware(LoggingMiddleware())
dp.include_routers(weather.router, basic.router, settings.router, universal.router)


async def main():
    init_db()
    await set_default_commands(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

