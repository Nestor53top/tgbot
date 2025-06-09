import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.enums import ContentType
from aiogram.filters import CommandStart
from aiogram import F
import asyncio
import logging

# Логирование (необязательно)
logging.basicConfig(level=logging.INFO)

# ✅ Получаем данные из переменных среды
API_TOKEN = os.getenv("8039622211:AAFAlP4a20MzceoPU7QsafkYkwlb3qLaMRs")
AUTHORIZED_USERS = {int(uid) for uid in os.getenv("1261999778", "").split(",") if uid.strip().isdigit()}

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
    user_id = msg.from_user.id
    if user_id in AUTHORIZED_USERS:
        await msg.answer("✅ Доступ открыт, добро пожаловать!", reply_markup=main_keyboard)
    else:
        await msg.answer("❌ Доступ запрещён.")

@dp.message(F.content_type.in_({ContentType.TEXT, ContentType.DOCUMENT}))
async def handle_input(msg: types.Message):
    user_id = msg.from_user.id
    if user_id not in AUTHORIZED_USERS:
        await msg.answer("⛔️ Нет доступа.")
        return

    if msg.text in ["📁 Файлы", "🔗 Ссылки", "💬 Сообщения"]:
        cat = msg.text
        data = user_storage
        if cat == "📁 Файлы":
            await msg.answer("🗂 Сохранённые файлы:\n" + "\n".join(data['files']) if data['files'] else "Пока нет файлов.")
        elif cat == "🔗 Ссылки":
            await msg.answer("🔗 Сохранённые ссылки:\n" + "\n".join(data['links']) if data['links'] else "Пока нет ссылок.")
        elif cat == "💬 Сообщения":
            await msg.answer("💬 Сохранённые сообщения:\n" + "\n".join(data['messages']) if data['messages'] else "Пока нет сообщений.")
        return

    if msg.document:
        user_storage['files'].append(f"{msg.from_user.username or msg.from_user.first_name}: {msg.document.file_name}")
        await msg.answer("Файл получен. (Сохраняется как 📁 Файлы)")
    elif msg.text.startswith("http://") or msg.text.startswith("https://"):
        user_storage['links'].append(f"{msg.from_user.username or msg.from_user.first_name}: {msg.text}")
        await msg.answer("Ссылка получена. (Сохраняется как 🔗 Ссылки)")
    else:
        user_storage['messages'].append(f"{msg.from_user.username or msg.from_user.first_name}: {msg.text}")
        await msg.answer("Сообщение получено. (Сохраняется как 💬 Сообщения)")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
if __name__ == "__main__":
    asyncio.run(main())

