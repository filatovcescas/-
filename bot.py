import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

API_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# 🔹 ГЛАВНОЕ МЕНЮ
def main_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🔍 Купить", callback_data="buy"),
        InlineKeyboardButton("🔑 Подключиться", callback_data="connect"),
        InlineKeyboardButton("💸 Реф. система", callback_data="ref"),
        InlineKeyboardButton("📞 Поддержка", callback_data="support"),
    )
    return kb


# 🔹 СТАРТ
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    text = (
        "👋 Привет!\n\n"
        "Здесь ты можешь оформить подписку на VPN — надёжный доступ к свободному интернету:\n\n"
        "🔥 Youtube без рекламы\n"
        "🔥 Обходи любые блокировки\n\n"
        "📍 Локации: 🇫🇮 🇩🇪 🇳🇱 🇪🇪 🇺🇸 🇷🇺\n\n"
        "💰 Гарантия возврата денег\n"
        "🔒 Полная анонимность\n\n"
    )
    await message.answer(text, reply_markup=main_menu())


# 🔹 ПОДКЛЮЧЕНИЕ
@dp.callback_query_handler(lambda c: c.data == "connect")
async def connect(callback: types.CallbackQuery):
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🍏 iPhone", callback_data="iphone"),
        InlineKeyboardButton("🤖 Android", callback_data="android"),
        InlineKeyboardButton("💻 Windows", callback_data="windows"),
        InlineKeyboardButton("🍏 Mac OS", callback_data="mac"),
        InlineKeyboardButton("📺 Android TV", callback_data="tv"),
        InlineKeyboardButton("📖 Руководство", callback_data="guide"),
        InlineKeyboardButton("🔙 Назад", callback_data="back"),
    )

    await callback.message.edit_text(
        "Ваш ключ:\nhttps://test-vpn-link\n\nВыберите устройство:",
        reply_markup=kb
    )


# 🔹 РЕФЕРАЛКА
@dp.callback_query_handler(lambda c: c.data == "ref")
async def ref(callback: types.CallbackQuery):
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("✈️ Поделиться", url="https://t.me"),
        InlineKeyboardButton("🔙 Назад", callback_data="back")
    )

    await callback.message.edit_text(
        "💸 Реферальная система\n\n"
        "Баланс: 0₽\n\n"
        "Ваша ссылка:\nhttps://t.me/test_vpn_bot",
        reply_markup=kb
    )


# 🔹 ПОДДЕРЖКА
@dp.callback_query_handler(lambda c: c.data == "support")
async def support(callback: types.CallbackQuery):
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("👨‍💻 Написать", url="https://t.me/your_username"),
        InlineKeyboardButton("🔙 Назад", callback_data="back")
    )

    await callback.message.edit_text(
        "📞 Поддержка\n\nНапишите нам, поможем!",
        reply_markup=kb
    )


# 🔹 КУПИТЬ
@dp.callback_query_handler(lambda c: c.data == "buy")
async def buy(callback: types.CallbackQuery):
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("💳 Оплатить", callback_data="pay"),
        InlineKeyboardButton("🔙 Назад", callback_data="back")
    )

    await callback.message.edit_text(
        "💰 Покупка VPN\n\nВыберите действие:",
        reply_markup=kb
    )


# 🔹 НАЗАД
@dp.callback_query_handler(lambda c: c.data == "back")
async def back(callback: types.CallbackQuery):
    await callback.message.edit_text("Главное меню:", reply_markup=main_menu())


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
