
from google.generativeai import configure, GenerativeModel #type: ignore

from config import GEMINI_API_KEY, GEMINI_MODEL


if not GEMINI_API_KEY:
    print("❌ GEMINI_API_KEY muhit o'zgaruvchisi o'rnatilmagan.\nIltimos Railway yoki mahalliy muhitda GEMINI_API_KEY ni sozlang.")
    raise SystemExit(1)

configure(api_key=GEMINI_API_KEY)
model = GenerativeModel(GEMINI_MODEL)


async def generate_ai_response(user_text):
    try:
        
        response = model.generate_content(user_text)

        
        if response.text:
            return response.text
        else:
            return "❌ Javob olinmadi. Qaytadan urinib ko'ring."

    except Exception as e:
        print(f"Gemini API xatosi: {e}")
        return None