from flask import Flask, request
import requests
import os
import logging

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TAWK_API_KEY = os.getenv('TAWK_API_KEY')
TAWK_PROPERTY_ID = os.getenv('TAWK_PROPERTY_ID')
TAWK_CHAT_ID = os.getenv('TAWK_CHAT_ID')
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET')

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route('/telegram_webhook', methods=['POST'])
def telegram_webhook():
    data = request.json
    logging.info('Telegram webhook received: %s', data)
    
    # Process the incoming message
    if 'message' in data:
        chat_id = data['message']['chat']['id']
        text = data['message']['text']
        
        # Forward the message to Tawk.to
        send_to_tawk(chat_id, text)
    
    return '', 200

def send_to_tawk(chat_id, text):
    tawk_url = f"https://api.tawk.to/chats/{TAWK_CHAT_ID}/messages"
    payload = {
        'message': text,
        'sender': 'telegram_bot',
        'chat_id': chat_id
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {TAWK_API_KEY}'
    }
    
    response = requests.post(tawk_url, json=payload, headers=headers)
    logging.info('Tawk.to response: %s', response.text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
