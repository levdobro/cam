from flask import Flask, request
import requests
import os
import time

app = Flask(__name__)

BOT_TOKEN = "8766113759:AAFIiGnaZRjFN8hhksqb0sjJMWtNl3u5LVk"
ADMIN_ID = "6802813322"

# Хранилище активных ПК-клиентов
active_pc = {}

def send_telegram(chat_id, text):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, json={'chat_id': chat_id, 'text': text})
    except:
        pass

@app.route('/pc-on', methods=['POST'])
def pc_on():
    data = request.get_json()
    chat_id = data.get('chat_id')
    if chat_id:
        active_pc[chat_id] = time.time()
        return {"ok": True}
    return {"ok": False}, 400

@app.route('/pc-off', methods=['POST'])
def pc_off():
    data = request.get_json()
    chat_id = data.get('chat_id')
    if chat_id and chat_id in active_pc:
        del active_pc[chat_id]
    return {"ok": True}

@app.route('/', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        if data and 'message' in data and 'text' in data['message']:
            chat_id = str(data['message']['chat']['id'])
            text = data['message']['text'].strip()
            
            if chat_id in active_pc:
                return "OK", 200
            
            if text == '/start':
                send_telegram(chat_id, "📄 Добро пожаловать в облачный редактор документов!")
            elif text == '/help':
                send_telegram(chat_id, "/new - создать документ\n/open - открыть\n/save - сохранить")
            elif text == '/new':
                send_telegram(chat_id, "✅ Новый документ создан")
        
        return "OK", 200
    except:
        return "OK", 200

@app.route('/')
def home():
    return "Cloud Document Editor API"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
