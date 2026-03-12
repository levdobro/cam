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
    except:
        pass

@app.route('/', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        
        if 'message' in data and 'text' in data['message']:
            chat_id = data['message']['chat']['id']
            text = data['message']['text'].strip()
            name = data['message']['from'].get('first_name', 'User')
            
            # ⚠️ НИКАКОГО ПАРОЛЯ В ОТВЕТАХ!
            if text == '/start':
                response = "👋 Добро пожаловать! Я дежурный бот.\nДля доступа к камерам нужна программа на ПК."
            elif text == '/help':
                response = "/start - приветствие\n/help - помощь\n/status - статус"
            elif text == '/status':
                response = "🟢 Дежурный бот работает"
            else:
                # Игнорируем все остальные сообщения (не отвечаем!)
                return "OK", 200
            
            send_telegram(chat_id, response)
            
            # Уведомление админу (только если сообщение не от админа)
            if str(chat_id) != ADMIN_ID and text not in ['/start', '/help', '/status']:
                send_telegram(ADMIN_ID, f"📩 {name}: {text}")
        
        return "OK", 200
    except:
        return "OK", 200

@app.route('/')
def home():
    return "Дежурный бот работает"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
