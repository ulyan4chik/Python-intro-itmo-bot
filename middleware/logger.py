import logging
import os
from aiogram import BaseMiddleware
from aiogram.types import Message, Update

os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename='logs/bot.log',
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
)


class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Update, data: dict):
        if isinstance(event, Message):
            logging.info(f"Message from {event.from_user.id} ({event.from_user.full_name}): {event.text}")
        return await handler(event, data)
