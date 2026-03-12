from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = "8766113759:AAFIiGnaZRjFN8hhksqb0sjJMWtNl3u5LVk"
ADMIN_ID = "6802813322"

def send_telegram(chat_id, text):
    """Отправка сообщения в Telegram"""
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, json={'chat_id': chat_id, 'text': text})
        print(f"✅ Отправлено {chat_id}")
    except Exception as e:
        print(f"❌ Ошибка отправки: {e}")

@app.route('/', methods=['POST'])
def webhook():
    """Точка входа для всех сообщений от Telegram (только POST)"""
    try:
        data = request.get_json()
        print(f"📨 Получен POST: {data}")

        if data and 'message' in data and 'text' in data['message']:
            chat_id = data['message']['chat']['id']
            text = data['message']['text'].strip()
            name = data['message']['from'].get('first_name', 'Пользователь')

            print(f"👤 {name} ({chat_id}): {text}")

            # Логика ответов
            if text == '/start':
                reply = "👋 Добро пожаловать! Бот работает 24/7\n🔑 Пароль: iguguana666"
            elif text == '/help':
                reply = "/start - приветствие\n/help - помощь\n/status - статус"
            elif text == '/status':
                reply = "🟢 Бот работает нормально"
            else:
                reply = "👋 Используй /help"

            send_telegram(chat_id, reply)

            # Уведомление админу
            if str(chat_id) != ADMIN_ID:
                send_telegram(ADMIN_ID, f"📩 {name}: {text}")

        return "OK", 200
    except Exception as e:
        print(f"❌ Ошибка в webhook: {e}")
        return "OK", 200

@app.route('/', methods=['GET'])
def home():
    """Страница для проверки в браузере"""
    return "<h1>🤖 Camera Bot работает!</h1><p>Бот активен и готов принимать сообщения.</p>"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
