import asyncio
import traceback
import sys
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from config import BOT_TOKEN, MESSAGES
from gemini import generate_ai_response

# Delay Bot construction so missing BOT_TOKEN doesn't crash the process on import.
bot = None
if BOT_TOKEN:
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
else:
    # Log a clear message but do NOT exit; keep the process alive so Railway won't restart it.
    print("❌ BOT_TOKEN muhit o'zgaruvchisi o'rnatilmagan.\nIltimos Railway yoki mahalliy muhitda BOT_TOKEN ni sozlang.\nBot polling boshlamaydi.")

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
        # If bot wasn't constructed because BOT_TOKEN is missing, don't call start_polling.
        if not bot:
            print("Bot token topilmadi — polling boshlamaydi. Ilovaga BOT_TOKEN qo'shilishini kutyapmiz.")
            # Block forever (keep container alive) until vars are fixed and process restarted.
            await asyncio.Event().wait()
        else:
            await dp.start_polling(bot)

    except Exception:
        print("❌ Xatolik yuz berdi. To'liq traceback quyida:")
        traceback.print_exc()
        print("API key larni tekshiring!")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Bot to'xtatildi!")
    finally:
        if bot:
            await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())