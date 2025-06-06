from aiogram import Router, F
from aiogram.types import Message
from db.connection import get_user, add_or_update_user
from handlers.weather import send_weather
from keyboards.inline_keyboard import language_keyboard
from keyboards.reply_keyboard import main_keyboard
from services.translator import t


router = Router(name="commands")
user_states = {}


@router.message(F.text == "/help")
async def help_handler(message: Message):
    await message.answer(t("msg_help", message.from_user.id))


@router.message(F.text == "/start")
async def start_handler(message: Message):
    user_id = message.from_user.id
    user = get_user(user_id)
    if not user:
        await message.answer(
            t("get_language", user_id),
            reply_markup=language_keyboard()
        )
        return

    if user[2] and user[3]:
        await message.answer(
            t("msg_start", user_id, name=user[3]),
            reply_markup=main_keyboard(user_id)
        )
    else:
        user_states[user_id] = "awaiting_city"
        await message.answer(t("msg_start_registration", user_id))


@router.message(F.text == "/weather")
async def weather_command_handler(message: Message):
    user = get_user(message.from_user.id)
    await send_weather(message, user[2])


@router.message(F.text == "/language")
async def language_handler(message: Message):
    await message.answer(t("get_language", message.from_user.id), reply_markup=language_keyboard())


@router.message(F.text == "/reset")
async def reset_handler(message: Message):
    add_or_update_user(
        user_id=message.from_user.id,
        user_name=message.from_user.full_name,
        city=None,
        custom_name=None
    )
    await message.answer(t("msg_successful_reset", message.from_user.id))


async def registration_flow(message: Message):
    user_id = message.from_user.id
    state = user_states.get(user_id)
    if state == "awaiting_city":
        user_states[user_id] = {"city": message.text.strip()}
        await message.answer(t("get_name", user_id))
    elif isinstance(state, dict) and "city" in state and "custom_name" not in state:
        state["custom_name"] = message.text.strip()
        user = get_user(user_id)
        lang = user[4] if user and user[4] else "ru"
        add_or_update_user(
            user_id=user_id,
            user_name=message.from_user.full_name,
            city=state["city"],
            custom_name=state["custom_name"],
            lang=lang
        )
        user_states.pop(user_id, None)
        await message.answer(t("msg_successful_registration", user_id, name=state["custom_name"]), reply_markup=main_keyboard(user_id))
