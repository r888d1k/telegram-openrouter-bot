import telebot
import time
import requests

# توكن البوت (Telegram Bot Token)
TOKEN = "8466485634:AAEaDpYw_ESPIfeuxDy3beJxM99Itwdj9hs"

# مفتاح API الخاص بـ OpenRouter
OPENROUTER_API_KEY = "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"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

bot = telebot.TeleBot(TOKEN)

# لتفادي إرسال الترحيب أكثر من مرة لنفس المستخدم
users_greeted = set()

# رسالة ترحيبية تُرسل مرة واحدة فقط
WELCOME_MSG = """\
هلا! 🙌
أنـا چات عالسريع، بوت أجاوبك على أسئلتك ونسولف سوا إذا تحب.
جرب تسألني أي شي بخاطرك، وأنا حاضر!

🤖 من برمجة وتطوير: Mohamed Ali
📬 للتواصل: @R8d1k
"""

# دالة ترسل الرسالة إلى OpenRouter وتستقبل الرد
def get_openrouter_response(user_message):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    json_data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": user_message}
        ],
        "max_tokens": 100,
        "temperature": 0.7
    }
    try:
        response = requests.post(OPENROUTER_URL, headers=headers, json=json_data, timeout=15)
        response.raise_for_status()
        data = response.json()
        reply = data['choices'][0]['message']['content'].strip()
        return reply
    except Exception as e:
        print("OpenRouter API error:", e)
        return "آسف، حدث خطأ أثناء معالجة طلبك. حاول مرة أخرى."

# التعامل مع كل رسالة واردة
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    text = message.text.strip()

    if chat_id not in users_greeted:
        bot.send_message(chat_id, WELCOME_MSG)
        users_greeted.add(chat_id)

    reply = get_openrouter_response(text)
    bot.send_message(chat_id, reply)

# حلقة التشغيل الدائمة مع معالجة الأخطاء
while True:
    try:
        print("البوت شغال...")
        bot.polling(non_stop=True)
    except Exception as e:
        print("خطأ في البوت:", e)
        time.sleep(10)
