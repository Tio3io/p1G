from flask import Flask, request
import os

app = Flask("__name__")

PI_ENDPOINT = "https://excrescently-ferrety-kimberlee.ngrok-free.dev"
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
    if not data:
        return "OK", 200

    try:
        for entry in data.get("entry",[]):
            for change in entry.get("changes", []):
                if change.get("field") == "messages":
                    messages = change["value"].get("messages", [])
                    for msg in messages:
                        requests.post(PI_ENDPOINT, json={"messages": [msg]}, timeout=10)
    except Exception as e:
        print("Err paring:", e)
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

