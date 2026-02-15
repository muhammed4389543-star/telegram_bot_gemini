
from google.generativeai import configure, GenerativeModel #type: ignore
from datetime import datetime

from config import GEMINI_API_KEY, GEMINI_MODEL


# Do not exit on import when the key is missing; fail gracefully at request time.
model = None
_gemini_configured = False
if GEMINI_API_KEY:
    try:
        configure(api_key=GEMINI_API_KEY)
        # Enable Google Search retrieval tool so the model can look up
        # facts and current events on the web.
        model = GenerativeModel(GEMINI_MODEL, tools=[{"google_search_retrieval": {}}])
        _gemini_configured = True
    except Exception as e:
        print(f"Gemini init error: {e}")
        _gemini_configured = False
else:
    # Log a clear message (but don't raise) so the process doesn't crash/restart.
    print("❌ GEMINI_API_KEY muhit o'zgaruvchisi o'rnatilmagan.\nIltimos Railway yoki mahalliy muhitda GEMINI_API_KEY ni sozlang.")


async def generate_ai_response(user_text):
    if not _gemini_configured or model is None:
        # Return a user-friendly message so the bot can respond instead of crashing.
        return "❌ Gemini API kaliti o'rnatilmagan yoki noto'g'ri. Iltimos admin bilan bog'laning."

    try:
        # Gemini ga so'rov yuborish
        # Include a dynamic system instruction with the current local datetime
        # so the model can reference the real current date/time when answering.
        now = datetime.now()
        system_instruction = f"Hozirgi sana va vaqt: {now.isoformat()}"

        # Some versions of the Google Generative API client may not accept a
        # `system_instruction` named parameter on generate_content. To avoid
        # compatibility errors we prepend the system instruction into the
        # prompt sent to the model instead of passing it as a separate arg.
        prompt = f"[SYSTEM INSTRUCTION]\n{system_instruction}\n\n{user_text}"
        response = model.generate_content(prompt)

        # Javobni olish
        if response and getattr(response, 'text', None):
            return response.text
        else:
            return "❌ Javob olinmadi. Qaytadan urinib ko'ring."

    except Exception as e:
        print(f"Gemini API xatosi: {e}")
        return None