import os


BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini model nomi
GEMINI_MODEL = "gemini-3-flash-preview"

# Xabarlar
MESSAGES = {
    "start": """
🤖 <b>Salom! Men Gemini AI Bot man!</b>

Menga har qanday savol yoki xabar yozing va men Google Gemini AI yordamida sizga javob beraman.

💡 <b>Misol savollar:</b>
• "Python da dasturlash haqida aytib ber"
• "Matematika masalasini yech"
• "She'r yoz"
• "Tarix haqida so'ra"

Har qanday mavzuda gaplashishimiz mumkin! 🚀
""",
    "thinking": "🤔 O'ylayapman...",
    "error": """
❌ <b>Xatolik yuz berdi!</b>

Iltimos, qaytadan urinib ko'ring yoki keyinroq murojaat qiling.
""",
    "no_text": """
📝 <b>Matn xabar yuboring!</b>

Men faqat matn xabarlarga javob bera olaman.
""",
    "help": """
❓ <b>Yordam</b>

<b>Qanday ishlaydi:</b>
1️⃣ Menga har qanday savol yoki xabar yozing
2️⃣ Men Google Gemini AI dan javob olaman
3️⃣ Bir necha soniyada sizga javob beraman

<b>Buyruqlar:</b>
/start - Botni qayta ishga tushirish
/help - Ushbu yordam xabari

<b>Maslahatlar:</b>
• Aniq savollar bering
• Uzun matnlar ham mumkin
• Har qanday tilda yozing

🤖 Men sizning shaxsiy AI yordamchingizman!
""",
}