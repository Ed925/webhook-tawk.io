import hashlib
import hmac
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

# Replace 'your_generated_secret' with the secret you generated
WEBHOOK_SECRET = 'dabeafa65b124c0913967e5c9b608f08'

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
    app.run(port=5000)
