from flask import Flask, request, abort
import requests
import os

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET')

@app.route('/webhook', methods=['POST'])
def webhook():
    # Validate the webhook secret
    received_secret = request.headers.get('X-Tawk-Signature')
    if received_secret != WEBHOOK_SECRET:
        abort(403)  # Forbidden
    
    data = request.json
    message = data.get('message', 'New event on Tawk.to')
    
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }
    requests.post(telegram_url, data=payload)
    
    return '', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
