from flask import Flask, request
import requests
import threading
import time
import os
from datetime import datetime

app = Flask(__name__)

# ========== ТВОИ ДАННЫЕ ==========
BOT_TOKEN = "8766113759:AAFIiGnaZRjFN8hhksqb0sjJMWtNl3u5LVk"
ADMIN_ID = "6802813322"
# ================================

# Хранилище сообщений
messages = []
last_update_id = 0
start_time = datetime.now()

def get_uptime():
    delta = datetime.now() - start_time
    hours = delta.seconds // 3600
    minutes = (delta.seconds % 3600) // 60
    return f"{delta.days}д {hours}ч {minutes}м"

def send_telegram(chat_id, text):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, json={'chat_id': chat_id, 'text': text}, timeout=3)
    except:
        pass

def check_messages():
    global last_update_id
    
    while True:
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
            params = {'offset': last_update_id + 1, 'timeout': 30}
            response = requests.get(url, params=params, timeout=35)
            
            if response.ok:
                data = response.json()
                if data['ok'] and data['result']:
                    for update in data['result']:
                        last_update_id = update['update_id']
                        
                        if 'message' in update and 'text' in update['message']:
                            chat_id = str(update['message']['chat']['id'])
                            text = update['message']['text'].strip()
                            name = update['message']['from'].get('first_name', 'User')
                            
                            print(f"📨 {name}: {text}")
                            
                            # Ответы на команды
                            if text == '/start':
                                response_text = "👋 Добро пожаловать! Я бот 24/7\n🔑 Пароль: iguguana666"
                            elif text == '/help':
                                response_text = "/start /help /status"
                            elif text == '/status':
                                response_text = f"🟢 Работаю {get_uptime()}"
                            else:
                                response_text = "👋 Используй /help"
                            
                            send_telegram(chat_id, response_text)
                            
                            # Уведомление админу
                            if chat_id != ADMIN_ID:
                                messages.append({
                                    'time': time.strftime('%Y-%m-%d %H:%M:%S'),
                                    'name': name,
                                    'text': text
                                })
                                send_telegram(ADMIN_ID, f"📩 {name}: {text}")
        except Exception as e:
            print(f"Ошибка: {e}")
        
        time.sleep(1)

@app.route('/')
def home():
    return f"""
    <html>
        <body>
            <h1>🤖 Camera Bot 24/7</h1>
            <p>🟢 Работает: {get_uptime()}</p>
            <p>📊 Сообщений: {len(messages)}</p>
        </body>
    </html>
    """

@app.route('/messages')
def view_messages():
    if not messages:
        return "Нет сообщений"
    html = "<h2>Последние сообщения:</h2><pre>"
    for msg in messages[-20:]:
        html += f"[{msg['time']}] {msg['name']}: {msg['text']}\n"
    return html

if __name__ == '__main__':
    threading.Thread(target=check_messages, daemon=True).start()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)