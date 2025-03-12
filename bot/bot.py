from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(token=TOKEN)
dp = Dispatcher()

kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Баг"), KeyboardButton(text="Предложение")],
    ],
    resize_keyboard=True
)

user_state = {}
user_messages = {}


@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Выберите категорию:", reply_markup=kb)


@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    text = message.text

    if text in ["Баг", "Предложение"]:
        user_state[user_id] = text
        await message.answer("Опишите вашу проблему:")
    elif user_id in user_state:
        category = user_state.pop(user_id)
        sent_message = await bot.send_message(
            ADMIN_ID, f"<b>{category}</b>\n\n{text}", parse_mode="HTML"
        )
        user_messages[sent_message.message_id] = user_id  # Запоминаем, кто отправил

        await message.answer("Сообщение отправлено в поддержку.", reply_markup=kb)

    elif message.chat.id == ADMIN_ID and message.reply_to_message:
        replied_message_id = message.reply_to_message.message_id

        if replied_message_id in user_messages:
            target_user = user_messages[replied_message_id]
            await bot.send_message(target_user, f"👤 <b>Ответ поддержки:</b>\n\n{message.text}", parse_mode="HTML")
            await message.answer("Ответ отправлен пользователю.")
        else:
            await message.answer("Не удалось определить получателя.")

    else:
        await message.answer("Выберите категорию.")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())