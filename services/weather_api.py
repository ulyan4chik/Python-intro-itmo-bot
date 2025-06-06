from datetime import datetime

import aiohttp
import asyncio
from config import WEATHER_API_KEY
from urllib.parse import quote

CACHE = {}


async def get_weather(city: str, lang: str = "ru"):
    cache_key = f"{city.lower()}_{lang}"
    if cache_key in CACHE:
        return CACHE[cache_key]
    encoded_city = quote(city)
    url = (
        f"https://api.openweathermap.org/data/2.5/weather?"
        f"q={encoded_city}&appid={WEATHER_API_KEY}&units=metric&lang={lang}"
    )
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, ssl=False, timeout=5) as response:
                if response.status != 200:
                    return f"⚠️ API error. Please try again later." if lang == "en" else "⚠️ Ошибка API. Попробуйте позже"
                data = await response.json()
                weather_data = {
                    "temperature": data["main"]["temp"],
                    "feels_like": data["main"]["feels_like"],
                    "description": data["weather"][0]["description"].capitalize(),
                    "pressure": data["main"]["pressure"],
                    "humidity": data["main"]["humidity"],
                    "wind_speed": data["wind"]["speed"],
                    "sunrise": datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M"),
                    "sunset": datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M"),
                }
                CACHE[cache_key] = weather_data
                return weather_data
    except (aiohttp.ClientError, asyncio.TimeoutError):
        return f"⚠️ Request error. Try again." if lang == "en" else "⚠️ Ошибка запроса. Попробуйте позже"
