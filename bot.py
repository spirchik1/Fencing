import os
import telebot
import requests

API_KEY = os.getenv("AI_API_KEY")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "📸 Привет! Я решаю задачи по ФОТО и ТЕКСТУ!\nПросто отправь мне фото или напиши задачу.")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    bot.reply_to(message, "⏳ Думаю...")
    response = requests.post(
        "https://apihub.agnes-ai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        json={
            "model": "agnes-2.0-flash",
            "messages": [
                {"role": "system", "content": "Ты — репетитор по математике. Реши задачу, дай ответ и объяснение по шагам."},
                {"role": "user", "content": message.text}
            ],
            "temperature": 0.3,
            "max_tokens": 2000
        }
    )
    answer = response.json()["choices"][0]["message"]["content"]
    bot.reply_to(message, answer)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.reply_to(message, "🔄 Распознаю задачу на фото...")
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_info.file_path}"
    response = requests.post(
        "https://apihub.agnes-ai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        json={
            "model": "agnes-2.0-flash",
            "messages": [
                {"role": "system", "content": "Ты — репетитор по математике. Распознай задачу на фото и реши её. Дай ответ и объяснение по шагам."},
                {"role": "user", "content": f"Реши задачу с этого фото: {file_url}"}
            ],
            "temperature": 0.3,
            "max_tokens": 2000
        }
    )
    answer = response.json()["choices"][0]["message"]["content"]
    bot.reply_to(message, answer)

print("Бот запущен и работает...")
bot.infinity_polling()
