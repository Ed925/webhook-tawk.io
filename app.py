import os
import hashlib
import hmac
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', 'your_generated_secret')  # Replace with your actual secret

def verify_signature(request):
    signature = request.headers.get('X-Hub-Signature-256')
    if not signature:
        return False

    sha_name, signature = signature.split('=')
    if sha_name != 'sha256':
        return False

    mac = hmac.new(WEBHOOK_SECRET.encode(), msg=request.data, digestmod=hashlib.sha256)
    return hmac.compare_digest(mac.hexdigest(), signature)

@app.route('/webhook', methods=['POST'])
def webhook():
    if not verify_signature(request):
        abort(400, 'Invalid signature')
    
    data = request.get_json()
    # Process the data (e.g., print it, store it in a database, etc.)
    print(data)
    # Respond to the webhook
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 10000))  # Use PORT environment variable or default to 10000
    app.run(host='0.0.0.0', port=port)
