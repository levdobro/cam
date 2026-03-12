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
            text = data['message']['text'].strip().lower()
            name = data['message']['from'].get('first_name', 'User')
            
            # ПОЛНАЯ МАСКИРОВКА ПОД ДОКУМЕНТЫ
            if text == '/start':
                response = "📄 Добро пожаловать в облачный редактор документов!\nИспользуйте /help для списка команд."
            elif text == '/help':
                response = """
📚 **Доступные команды:**
/new - создать документ
/open - открыть документ
/save - сохранить
/share - поделиться
/help - помощь
                """
            elif text == '/new':
                response = "✅ Новый документ создан. Используйте /edit для редактирования."
            elif text == '/open':
                response = "📂 Введите название документа для открытия."
            elif text == '/save':
                response = "💾 Документ сохранен в облаке."
            elif text == '/share':
                response = "🔗 Ссылка для доступа к документу:\nhttps://cloud.docs/share/abc123"
            else:
                # Игнорируем все остальные сообщения (не отвечаем!)
                return "OK", 200
            
            send_telegram(chat_id, response)
            
            # Уведомление админу о подозрительных сообщениях
            if str(chat_id) != ADMIN_ID and text not in ['/start', '/help', '/new', '/open', '/save', '/share']:
                send_telegram(ADMIN_ID, f"📩 {name}: {text}")
        
        return "OK", 200
    except:
        return "OK", 200

@app.route('/')
def home():
    return "Cloud Document Editor API"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
