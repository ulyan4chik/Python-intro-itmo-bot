from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from handlers.basic import start_handler
from keyboards.inline_keyboard import language_keyboard
from keyboards.reply_keyboard import main_keyboard, settings_keyboard, restart_keyboard, edit_keyboard
from db.connection import add_or_update_user, get_user, delete_user
from services.translator import t

router = Router(name="settings")
user_settings_state = {}
user_input_buffer = {}


@router.message(lambda msg: msg.text == t("btn_settings", msg.from_user.id))
async def show_settings(message: Message):
    await message.answer(t("btn_settings", message.from_user.id), reply_markup=settings_keyboard(message.from_user.id))


@router.message(lambda msg: msg.text == t("btn_edit_data", msg.from_user.id))
async def show_edit_menu(message: Message):
    await message.answer(t("msg_settings_change_data", message.from_user.id), reply_markup=edit_keyboard(message.from_user.id))


@router.message(lambda msg: msg.text == t("btn_change_city", msg.from_user.id))
async def ask_new_city(message: Message):
    user_settings_state[message.from_user.id] = "change_city"
    await message.answer(t("change_city", message.from_user.id))


@router.message(lambda msg: msg.text == t("btn_change_name", msg.from_user.id))
async def ask_new_name(message: Message):
    user_settings_state[message.from_user.id] = "change_name"
    await message.answer(t("change_name", message.from_user.id))


@router.message(lambda msg: msg.text == t("btn_change_language", msg.from_user.id))
async def ask_new_city(message: Message):
    await message.answer(t("change_language", message.from_user.id), reply_markup=language_keyboard())


@router.message(lambda msg: msg.text == t("btn_reset_data", msg.from_user.id))
async def reset_user_data(message: Message):
    add_or_update_user(user_id=message.from_user.id, user_name=message.from_user.full_name, city=None, custom_name=None)
    await message.answer(t("msg_successful_reset", message.from_user.id), reply_markup=restart_keyboard(message.from_user.id))


@router.message(lambda msg: msg.text == t("btn_help", msg.from_user.id))
async def show_help(message: Message):
    await message.answer(t("msg_help", message.from_user.id), parse_mode="HTML")


@router.message(lambda msg: msg.text == t("btn_restart", msg.from_user.id))
async def restart_handler(message: Message):
    delete_user(message.from_user.id)
    await start_handler(message)


@router.callback_query(F.data.startswith("lang_"))
async def set_language(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang_code = callback.data.split("_")[1]
    user = get_user(user_id)
    if not user:
        add_or_update_user(
            user_id=user_id,
            user_name=callback.from_user.full_name,
            city=None,
            custom_name=None,
            lang=lang_code
        )
        from handlers.basic import user_states
        user_states[user_id] = "awaiting_city"
        await callback.message.edit_text(t("msg_start_registration", user_id), reply_markup=None)
    else:
        add_or_update_user(
            user_id=user_id,
            user_name=user[1],
            city=user[2],
            custom_name=user[3],
            lang=lang_code
        )
        await callback.message.edit_text(t("msg_successful_updated_language", user_id))
        await callback.message.answer(t("msg_back", user_id), reply_markup=main_keyboard(user_id))
    await callback.answer()


@router.message(lambda msg: msg.text == t("btn_back", msg.from_user.id))
async def back_to_main(message: Message):
    await message.answer(t("msg_back", message.from_user.id), reply_markup=main_keyboard(message.from_user.id))


async def handle_settings_input(message: Message):
    state = user_settings_state.get(message.from_user.id)
    if state == "change_city":
        user = get_user(message.from_user.id)
        add_or_update_user(
            user_id=message.from_user.id,
            user_name=user[1],
            city=message.text.strip(),
            custom_name=user[3],
            lang=user[4]
        )
        user_settings_state.pop(message.from_user.id, None)
        await message.answer(t("msg_successful_updated_city", message.from_user.id), reply_markup=settings_keyboard(message.from_user.id))
    elif state == "change_name":
        user = get_user(message.from_user.id)
        add_or_update_user(
            user_id=message.from_user.id,
            user_name=user[1],
            city=user[2],
            custom_name=message.text.strip(),
            lang=user[4]
        )
        user_settings_state.pop(message.from_user.id, None)
        await message.answer(t("msg_successful_updated_name", message.from_user.id), reply_markup=settings_keyboard(message.from_user.id))
    elif state == "change_language":
        user = get_user(message.from_user.id)
        add_or_update_user(
            user_id=message.from_user.id,
            user_name=user[1],
            city=user[2],
            custom_name=message.text.strip(),
            lang=user[4]
        )
        user_settings_state.pop(message.from_user.id, None)
        await message.answer(t("msg_successful_updated_language", message.from_user.id), reply_markup=settings_keyboard(message.from_user.id))