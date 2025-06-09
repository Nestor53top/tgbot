
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.enums import ContentType
from aiogram.filters import CommandStart
from aiogram import F
import asyncio
import logging

# Включаем логирование
logging.basicConfig(filename="bot_log.txt", level=logging.INFO, format="%(asctime)s - %(message)s")

API_TOKEN = '8039622211:AAFAlP4a20MzceoPU7QsafkYkwlb3qLaMRs'
AUTHORIZED_USERS = {1261999778}

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

user_storage = {
    'files': [],
    'links': [],
    'messages': []
}

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📁 Файлы"), KeyboardButton(text="🔗 Ссылки")],
        [KeyboardButton(text="💬 Сообщения")]
    ],
    resize_keyboard=True
)

@dp.message(CommandStart())
async def start(msg: types.Message):
    await msg.answer("Проверка...")
    user_id = msg.from_user.id
    if user_id in AUTHORIZED_USERS:
        await msg.answer("✅ Доступ открыт, добро пожаловать! 🖐", reply_markup=main_keyboard)
    else:
        await msg.answer("❌ Доступ для вас закрыт, до свидания!")

@dp.message(F.content_type.in_({ContentType.TEXT, ContentType.DOCUMENT}))
async def handle_input(msg: types.Message):
    user_id = msg.from_user.id
    if user_id not in AUTHORIZED_USERS:
        await msg.answer("⛔️ Нет доступа.")
        return

    if msg.text in ["📁 Файлы", "🔗 Ссылки", "💬 Сообщения"]:
        category = msg.text
        data = user_storage
        if category == "📁 Файлы":
            await msg.answer("🗂 Сохранённые файлы:\n" + "\n".join(data['files']) if data['files'] else "Пока нет файлов.")
        elif category == "🔗 Ссылки":
            await msg.answer("🔗 Сохранённые ссылки:\n" + "\n".join(data['links']) if data['links'] else "Пока нет ссылок.")
        elif category == "💬 Сообщения":
            await msg.answer("💬 Сохранённые сообщения:\n" + "\n".join(data['messages']) if data['messages'] else "Пока нет сообщений.")
        return

    if msg.document:
        file_name = msg.document.file_name
        user_storage['files'].append(f"{msg.from_user.username or msg.from_user.first_name}: {file_name}")
        await msg.answer("Файл получен. В какую вкладку сохранить?\n(по умолчанию: 📁 Файлы)")
    elif msg.text.startswith("http://") or msg.text.startswith("https://"):
        user_storage['links'].append(f"{msg.from_user.username or msg.from_user.first_name}: {msg.text}")
        await msg.answer("Ссылка получена. В какую вкладку сохранить?\n(по умолчанию: 🔗 Ссылки)")
    else:
        user_storage['messages'].append(f"{msg.from_user.username or msg.from_user.first_name}: {msg.text}")
        await msg.answer("Сообщение получено. В какую вкладку сохранить?\n(по умолчанию: 💬 Сообщения)")

async def main():
    logging.info("Бот запущен.")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Ошибка запуска: {e}")

if __name__ == '__main__':
    asyncio.run(main())
