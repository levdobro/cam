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
        return {"ok": True, "message": "PC active"}
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

@app.route('/pc-status', methods=['GET'])
def pc_status():
    """Проверка, активна ли ПК-программа для пользователя"""
    chat_id = request.args.get('chat_id')
    if chat_id and chat_id in active_pc:
        return {"active": True}
    return {"active": False}

@app.route('/', methods=['POST'])
def webhook():
    """Основной обработчик сообщений"""
    try:
        data = request.get_json()
        
        if 'message' in data and 'text' in data['message']:
            chat_id = str(data['message']['chat']['id'])
            text = data['message']['text'].strip()
            name = data['message']['from'].get('first_name', 'User')
            
            # Проверяем, активна ли ПК-программа для этого пользователя
            if chat_id in active_pc:
                # Если ПК активна - НЕ ОТВЕЧАЕМ, пусть она обрабатывает
                print(f"⏭️ Сообщение от {name} перенаправлено в ПК")
                return "OK", 200
            
            # Если ПК не активна - отвечаем как документ-бот
            print(f"📄 {name}: {text} (обработано Render)")
            
            if text == '/start':
                response = "📄 Добро пожаловать в облачный редактор документов!\nИспользуйте /help для списка команд."
            elif text == '/help':
                response = """
📚 Доступные команды:
/new - создать документ
/open - открыть документ
/save - сохранить
/share - поделиться
/help - помощь
                """
            elif text == '/new':
                response = "✅ Новый документ создан."
            elif text == '/open':
                response = "📂 Введите название документа."
            elif text == '/save':
                response = "💾 Документ сохранен."
            elif text == '/share':
                response = "🔗 Ссылка: https://cloud.docs/share/abc123"
            else:
                # Не отвечаем на неизвестные команды
                return "OK", 200
            
            send_telegram(chat_id, response)
        
        return "OK", 200
    except Exception as e:
        print(f"Ошибка: {e}")
        return "OK", 200

@app.route('/')
def home():
    return """
    <html>
        <head><title>Cloud Document Editor</title></head>
        <body>
            <h1>📄 Cloud Document Editor API</h1>
            <p>Сервис работает</p>
        </body>
    </html>
    """

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
