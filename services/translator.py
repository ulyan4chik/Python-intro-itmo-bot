from db.connection import get_user
from locales.translations import TRANSLATIONS


def t(key: str, user_id: int, **kwargs) -> str:
    user = get_user(user_id)
    lang = user[4] if user else "ru"
    template = TRANSLATIONS.get(key, {}).get(lang, "")
    return template.format(**kwargs)
