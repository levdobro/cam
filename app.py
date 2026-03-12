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
    """Сигнал от ПК-программы, что она запущена"""
    data = request.get_json()
    chat_id = data.get('chat_id')
    if chat_id:
        active_pc[chat_id] = time.time()
        print(f"✅ ПК активен для {chat_id}")
        return {"ok": True}
    return {"ok": False}, 400

@app.route('/pc-off', methods=['POST'])
def pc_off():
    """Сигнал от ПК-программы, что она выключена"""
    data = request.get_json()
    chat_id = data.get('chat_id')
    if chat_id and chat_id in active_pc:
        del active_pc[chat_id]
        print(f"❌ ПК отключен для {chat_id}")
    return {"ok": True}

@app.route('/', methods=['POST'])
def webhook():
    """Основной обработчик сообщений"""
    try:
        data = request.get_json()
        
        if 'message' in data and 'text' in data['message']:
            chat_id = str(data['message']['chat']['id'])
            text = data['message']['text'].strip()
            name = data['message']['from'].get('first_name', 'User')
            
            # Если ПК активна - не отвечаем
            if chat_id in active_pc:
                print(f"⏭️ {name}: {text} -> в ПК")
                return "OK", 200
            
            # Иначе отвечаем как документ-бот
            print(f"📄 {name}: {text}")
            
            if text == '/start':
                response = "📄 Добро пожаловать в облачный редактор документов!"
            elif text == '/help':
                response = "/new - создать документ\n/open - открыть\n/save - сохранить"
            elif text == '/new':
                response = "✅ Новый документ создан"
            else:
                return "OK", 200
            
            send_telegram(chat_id, response)
        
        return "OK", 200
    except:
        return "OK", 200

@app.route('/')
def home():
    return "Cloud Document Editor API"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
