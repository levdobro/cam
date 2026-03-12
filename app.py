from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = "8766113759:AAFIiGnaZRjFN8hhksqb0sjJMWtNl3u5LVk"
ADMIN_ID = "6802813322"

def send_telegram(chat_id, text):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, json={'chat_id': chat_id, 'text': text})
        print(f"✅ Отправлено {chat_id}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

@app.route('/', methods=['POST'])
def webhook():
    """Обработка входящих сообщений от Telegram"""
    try:
        data = request.get_json()
        print(f"📨 Получено: {data}")
        
        if 'message' in data and 'text' in data['message']:
            chat_id = data['message']['chat']['id']
            text = data['message']['text'].strip()
            name = data['message']['from'].get('first_name', 'User')
            
            print(f"📨 {name}: {text}")
            
            # Ответы на команды
            if text == '/start':
                response = "👋 Добро пожаловать! Бот работает 24/7\n🔑 Пароль: iguguana666"
            elif text == '/help':
                response = "/start - приветствие\n/help - помощь\n/status - статус"
            elif text == '/status':
                response = "🟢 Бот работает нормально"
            else:
                response = "👋 Используй /help"
            
            send_telegram(chat_id, response)
            
            # Уведомление админу
            if str(chat_id) != ADMIN_ID:
                send_telegram(ADMIN_ID, f"📩 {name}: {text}")
        
        return "OK", 200
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return "OK", 200

@app.route('/', methods=['GET'])
def home():
    """Проверка что бот работает"""
    return """
    <html>
        <head><title>Camera Bot</title></head>
        <body>
            <h1>🤖 Camera Bot работает!</h1>
            <p>Бот активен и готов принимать сообщения.</p>
        </body>
    </html>
    """

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
