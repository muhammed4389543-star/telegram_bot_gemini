import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from config import BOT_TOKEN, MESSAGES
from gemini import generate_ai_response

if not BOT_TOKEN:
    print("❌ BOT_TOKEN muhit o'zgaruvchisi o'rnatilmagan.\nIltimos Railway yoki mahalliy muhitda BOT_TOKEN ni sozlang.")
    raise SystemExit(1)

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(MESSAGES["start"])


@dp.message(Command("help"))
async def help_handler(message: Message):
    await message.answer(MESSAGES["help"])


@dp.message(F.text)
async def text_message_handler(message: Message):
    user_text = message.text


    if user_text.startswith('/'):
        return


    thinking_msg = await message.answer(MESSAGES["thinking"])

    try:

        
        response = await generate_ai_response(user_text)

        
        await thinking_msg.delete()

        if response:
            
            await message.answer(response)
            print(f"Javob yuborildi: {len(response)} belgili")
        else:
            
            await message.answer(MESSAGES["error"])

    except Exception as e:
        print(f"Xatolik: {e}")
        await thinking_msg.delete()
        await message.answer(MESSAGES["error"])


@dp.message()
async def other_messages_handler(message: Message):
    await message.answer(MESSAGES["no_text"])


async def main():
    print("🤖 Gemini AI Bot ishga tushmoqda...")
    print("To'xtatish uchun Ctrl+C bosing")

    try:

        await dp.start_polling(bot)

    except Exception as e:
        print(f"❌ Xatolik: {e}")
        print("API key larni tekshiring!")
    except KeyboardInterrupt:
        print("\n👋 Bot to'xtatildi!")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())