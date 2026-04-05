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
        "📍 Локации: 🇷🇺 🇳🇱\n\n"
        "💰 Гарантия возврата денег\n"
        "🔒 Полная анонимность\n\n"
    )
    await message.answer(text, reply_markup=main_menu())


# 🔹 ПОДКЛЮЧЕНИЕ (КАК НА СКРИНЕ)
@dp.callback_query_handler(lambda c: c.data == "connect")
async def connect(callback: types.CallbackQuery):

    kb = InlineKeyboardMarkup(row_width=2)

    kb.add(
        InlineKeyboardButton("🍏 iPhone", url="https://apps.apple.com/ru/app/happ-proxy-utility-plus/id6746188973"),
        InlineKeyboardButton("🤖 Android", url="https://happ.press/"),
    )

    kb.add(
        InlineKeyboardButton("🍏 Mac OS", url="https://happ.press/"),
        InlineKeyboardButton("💻 Windows", url="https://happ.press/"),
    )

    kb.add(
        InlineKeyboardButton("📺 Apple TV", url="https://happ.press/"),
        InlineKeyboardButton("📺 Android TV", url="https://happ.press/"),
    )

    kb.add(
        InlineKeyboardButton("📖 Подробное руководство", url="https://happ.press/")
    )

    kb.add(
        InlineKeyboardButton("⚙️ Альтернативные приложения", url="https://happ.press/")
    )

    kb.add(
        InlineKeyboardButton("🔙 В главное меню", callback_data="back")
    )

    await callback.message.edit_text(
        "📲 Выберите своё устройство для подключения",
        reply_markup=kb
    )


# 🔹 РЕФЕРАЛКА
@dp.callback_query_handler(lambda c: c.data == "ref")
async def ref(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(
            "✈️ Поделиться!",
            url=f"https://t.me/share/url?url=https://t.me/test_vpn_bot?start={user_id}"
        ),
        InlineKeyboardButton("🔙 Назад", callback_data="back")
    )

    text = (
        "💸 Реферальная система\n"
        "💰 Баланс: 0₽\n\n"
        f"🆔 {user_id}\n\n"
        "🔗 Ссылка для приглашения:\n"
        f"https://t.me/test_vpn_bot?start={user_id}\n\n"
        "🎁 Получи 20% на баланс!\n"
        "За каждое пополнение друга — 20% тебе."
    )

    await callback.message.edit_text(text, reply_markup=kb)


# 🔹 ПОДДЕРЖКА (С АВТО-ТЕКСТОМ)
@dp.callback_query_handler(lambda c: c.data == "support")
async def support(callback: types.CallbackQuery):

    msg = "Здравствуйте нужна помощь с вашим ВПН"

    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(
            "👨‍💻 Написать",
            url=f"https://t.me/BaksbannyPro?text={msg}"
        ),
        InlineKeyboardButton("🔙 Назад", callback_data="back")
    )

    await callback.message.edit_text(
        "📞 Поддержка\n\nНажмите кнопку ниже и сообщение отправится автоматически:",
        reply_markup=kb
    )


# 🔹 КУПИТЬ (ОБНОВЛЕННЫЙ)
@dp.callback_query_handler(lambda c: c.data == "buy")
async def buy(callback: types.CallbackQuery):

    text = (
        "Выберите период премиум подписки:\n\n"
        "1 месяц — 169 ₽\n"
        "3 месяца — 469 ₽\n"
        "6 месяцев — 1169 ₽\n"
        "12 месяцев — 1999 ₽\n"
    )

    kb = InlineKeyboardMarkup(row_width=2)

    msg = "Здравствуйте хочу купить у вас Ключ ВПН"

    kb.add(
        InlineKeyboardButton(
            "🔑 Купить дополнительный ключ",
            url=f"https://t.me/BaksbannyPro?text={msg}"
        )
    )

    kb.add(
        InlineKeyboardButton(
            "1 месяц - 169 ₽",
            url=f"https://t.me/BaksbannyPro?text={msg}"
        ),
        InlineKeyboardButton(
            "3 месяца - 469 ₽",
            url=f"https://t.me/BaksbannyPro?text={msg}"
        ),
        InlineKeyboardButton(
            "6 месяцев - 1169 ₽",
            url=f"https://t.me/BaksbannyPro?text={msg}"
        ),
        InlineKeyboardButton(
            "1 год - 1999 ₽",
            url=f"https://t.me/BaksbannyPro?text={msg}"
        ),
    )

    kb.add(
        InlineKeyboardButton("🔙 Назад", callback_data="back")
    )

    await callback.message.edit_text(text, reply_markup=kb)


# 🔹 НАЗАД
@dp.callback_query_handler(lambda c: c.data == "back")
async def back(callback: types.CallbackQuery):
    await callback.message.edit_text("Главное меню:", reply_markup=main_menu())


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
