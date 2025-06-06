from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def language_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Русский 🇷🇺", callback_data="lang_ru"),
            InlineKeyboardButton(text="English 🇬🇧", callback_data="lang_en")
        ]
    ])
