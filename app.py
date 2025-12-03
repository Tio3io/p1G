from flask import Flask, request
import os

app = Flask("__name__")

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "my_verify_token")

@app.route('/webhook', methods=['GET'])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Verification failed", 403

@app.route('/webhook', methods=['POST'])
def receive_update():
    data = request.get_json(silent=True)
    # GET NOTIFICATIONS HERE
    print("Webhook event received:", data)
    return "OK", 200

if __name__ == "__main__":
    app.run()
