from aiogram import Router
from aiogram.types import Message
from services.weather_api import get_weather
from db.connection import get_user, get_weather_answer
from services.translator import t

router = Router(name="weather")
user_input_buffer = {}


@router.message(lambda msg: msg.text == t("btn_weather_now", msg.from_user.id))
async def weather_handler(message: Message):
    user = get_user(message.from_user.id)
    if user and user[2]:
        await send_weather(message, user[2])
    else:
        user_input_buffer[message.from_user.id] = "awaiting_city_set"
        await message.answer(t("get_city_weather", message.from_user.id))


async def send_weather(message: Message, city: str):
    user = get_user(message.from_user.id)
    weather = await get_weather(city, user[4])
    if not weather:
        await message.answer(t("err_weather", message.from_user.id))
        return
    msg = (
        f"{t('weather_intro', message.from_user.id)} <b>{city}</b>\n\n"
        f"❖ {t('weather_now', message.from_user.id)} {weather['description'].lower()}\n"
        f"❖ {t('weather_temperature', message.from_user.id)}: {weather['temperature']}°C ({t('feels_like', message.from_user.id)} {weather['feels_like']}°C)\n"
        f"❖ {t('weather_wind', message.from_user.id)}: {weather['wind_speed']}\n"
        f"❖ {t('weather_humidity', message.from_user.id)}: {weather['humidity']}%\n"
        f"❖ {t('weather_pressure', message.from_user.id)}: {weather['pressure']}\n\n"
        f"🔸 {t('weather_sunrise', message.from_user.id)}: {weather['sunrise']}\n"
        f"🔸 {t('weather_sunset', message.from_user.id)}: {weather['sunset']}\n"
    )
    msg2 = get_weather_answer(weather['description'].lower(), message.from_user.id)
    await message.answer(msg + "\n" + msg2, parse_mode="HTML")

