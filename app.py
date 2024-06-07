import os
import hashlib
import hmac
from flask import Flask, request, jsonify, abort
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
from telegram.ext.dispatcher import run_async

app = Flask(__name__)

# Get the environment variables
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', 'your_generated_secret')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# Initialize the bot and dispatcher
bot = Bot(token=TELEGRAM_TOKEN)
dispatcher = Dispatcher(bot, None, workers=0)

def verify_signature(request):
    signature = request.headers.get('X-Hub-Signature-256')
    if not signature:
        return False

    sha_name, signature = signature.split('=')
    if sha_name != 'sha256':
        return False

    mac = hmac.new(WEBHOOK_SECRET.encode(), msg=request.data, digestmod=hashlib.sha256)
    return hmac.compare_digest(mac.hexdigest(), signature)

# Define a command handler
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I'm a bot.")

# Define a message handler
def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

# Add handlers to dispatcher
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

@app.route('/webhook', methods=['POST'])
def webhook():
    if not verify_signature(request):
        abort(400, 'Invalid signature')

    data = request.get_json()
    update = Update.de_json(data, bot)
    dispatcher.process_update(update)
    return jsonify({"status": "success"}), 200

@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    webhook_url = f"https://webhook.site/f7caa9ff-c71a-4ade-835e-9aaa9935965d"
    bot.set_webhook(url=webhook_url)
    return "Webhook set"

if __name__ == '__main__':
    port = int(os.getenv('PORT', 10000))  # Use PORT environment variable or default to 5000
    app.run(host='0.0.0.0', port=port)
