from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from services.translator import t


def main_keyboard(user_id: int) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t("btn_weather_now", user_id))],
            [KeyboardButton(text=t("btn_settings", user_id))]
        ],
        resize_keyboard=True
    )


def settings_keyboard(user_id: int) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t("btn_edit_data", user_id)), KeyboardButton(text=t("btn_reset_data", user_id))],
            [KeyboardButton(text=t("btn_help", user_id)), KeyboardButton(text=t("btn_back", user_id))],
        ],
        resize_keyboard=True
    )


def edit_keyboard(user_id: int) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t("btn_change_city", user_id)), KeyboardButton(text=t("btn_change_name", user_id)), KeyboardButton(text=t("btn_change_language", user_id))],
            [KeyboardButton(text=t("btn_change_lang", user_id)), KeyboardButton(text=t("btn_back", user_id))],
        ],
        resize_keyboard=True
    )


def restart_keyboard(user_id: int) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=t("btn_restart", user_id))]],
        resize_keyboard=True
    )
