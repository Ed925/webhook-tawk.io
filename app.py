from flask import Flask, request
import requests
import os
import logging

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TAWK_API_KEY = os.getenv('TAWK_API_KEY')
TAWK_PROPERTY_ID = os.getenv('TAWK_PROPERTY_ID')
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET')

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    logging.info('Telegram webhook received: %s', data)
    
    # Process the incoming message
    if 'message' in data:
        chat_id = data['message']['chat']['id']
        text = data['message']['text']
        
        # Forward the message to Tawk.to
        send_to_tawk(text)
    
    return '', 200

def send_to_tawk(text):
    tawk_url = f"https://api.tawk.to/property/{TAWK_PROPERTY_ID}/conversations"
    payload = {
        'text': text,
        'sender': 'telegram_bot'
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {TAWK_API_KEY}'
    }
    
    response = requests.post(tawk_url, json=payload, headers=headers)
    logging.info('Tawk.to response: %s', response.text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
