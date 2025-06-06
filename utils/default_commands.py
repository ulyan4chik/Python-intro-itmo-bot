from aiogram import Bot
from aiogram.types import BotCommand


def set_default_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Запуск/Launch"),
        BotCommand(command="help", description="Помощь/Help"),
        BotCommand(command="weather", description="Узнать погоду/Get the weather"),
        BotCommand(command="language", description="Сменить язык/Change language"),
        BotCommand(command="reset", description="Сбросить данные/Reset data"),
    ]
    return bot.set_my_commands(commands)
