from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    # Process the data (e.g., print it, store it in a database, etc.)
    print(data)
    # Respond to the webhook
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(port=5000)
