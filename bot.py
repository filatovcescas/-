import logging
import sqlite3
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

API_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# База данных
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    referrer_id INTEGER
)
""")
conn.commit()

# Главное меню
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(
    KeyboardButton("🔍 Купить"),
    KeyboardButton("🔑 Подключиться")
)
main_menu.add(
    KeyboardButton("💸 Реферальная система"),
    KeyboardButton("📞 Поддержка")
)

# /start команда (с рефералкой)
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id
    args = message.get_args()

    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user = cursor.fetchone()

    if not user:
        referrer_id = None

        if args and args.isdigit():
            referrer_id = int(args)

        cursor.execute(
            "INSERT INTO users (user_id, referrer_id) VALUES (?, ?)",
            (user_id, referrer_id)
        )
        conn.commit()

    await message.answer(
        "👋 Привет!\n\n"
        "Добро пожаловать в Test VPN 🔐\n\n"
        "Выберите действие:",
        reply_markup=main_menu
    )

# Реферальная система
@dp.message_handler(lambda message: message.text == "💸 Реферальная система")
async def referral(message: types.Message):
    user_id = message.from_user.id

    cursor.execute("SELECT COUNT(*) FROM users WHERE referrer_id=?", (user_id,))
    count = cursor.fetchone()[0]

    bot_info = await bot.get_me()
    ref_link = f"https://t.me/{bot_info.username}?start={user_id}"

    await message.answer(
        f"💸 Ваша ссылка:\n{ref_link}\n\n"
        f"👥 Приглашено: {count}",
        reply_markup=main_menu
    )

# Купить
@dp.message_handler(lambda message: message.text == "🔍 Купить")
async def buy(message: types.Message):
    await message.answer(
        "💰 Тарифы скоро появятся",
        reply_markup=main_menu
    )

# Подключиться
@dp.message_handler(lambda message: message.text == "🔑 Подключиться")
async def connect(message: types.Message):
    await message.answer(
        "🔑 Доступ:\nhttps://example.com",
        reply_markup=main_menu
    )

# Поддержка
@dp.message_handler(lambda message: message.text == "📞 Поддержка")
async def support(message: types.Message):
    await message.answer(
        "📞 Поддержка:\n@your_username",
        reply_markup=main_menu
    )

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
