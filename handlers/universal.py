from aiogram import Router
from aiogram.types import Message
from handlers.basic import registration_flow, user_states
from handlers.settings import user_settings_state, handle_settings_input
from handlers.weather import user_input_buffer
from services.translator import t

router = Router(name="universal")


@router.message()
async def universal_input_handler(message: Message):
    uid = message.from_user.id
    if uid in user_settings_state:
        await handle_settings_input(message)
    elif uid in user_states:
        await registration_flow(message)
    elif uid in user_input_buffer:
        await registration_flow(message)
    else:
        await message.answer(t("msg_unknown_command", uid))


