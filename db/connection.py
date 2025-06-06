import sqlite3
import random
from config import DB_PATH


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            user_name TEXT,
            city TEXT,
            custom_name TEXT,
            language TEXT DEFAULT 'ru'
        )
        ''')
        conn.commit()


def get_user(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        return cursor.fetchone()


def add_or_update_user(user_id, user_name, city, custom_name, lang='ru'):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO users (user_id, user_name, city, custom_name, language)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            user_name = excluded.user_name,
            city = excluded.city,
            custom_name = excluded.custom_name,
            language = excluded.language
        ''', (user_id, user_name, city, custom_name, lang))
        conn.commit()


def delete_user(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        conn.commit()


def get_weather_answer(description: str, user_id: int) -> str:
    description = description.lower()
    lang = "ru"
    try:
        user = get_user(user_id)
        if user and len(user) >= 5 and user[4]:
            lang = user[4]
        key_column = "key_en" if lang == "en" else "key_ru"
        text_column = "en" if lang == "en" else "ru"
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"SELECT {text_column} FROM answer WHERE {key_column} LIKE ?",
                (f"%{description}%",)
            )
            jokes = [row[0] for row in cursor.fetchall() if row[0]]
            if jokes:
                return random.choice(jokes)
    except Exception as e:
        return (f"DB error: {e}")
    return "\nКакая бы ни была погода — настрой делаем мы!" if lang == "ru" else "\nWhatever the weather — we set the vibe!"
