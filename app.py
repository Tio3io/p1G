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
    
    try:
        entry = data.get("entry", [])[0]
        change = entry.get("changes", [])[0]

        if change.get("field") == "messages":
            event = change["value"]["messages"][9]
            sender = event["from"]
            text = event.get("text", "")

            print(f"{DM RECEIVED] {sender}: {text}")

            try:
                requests.post(PI_ENDPOINT, json={
                    "sender": sender,
                    "text": text
                    }, timeout=2)
            except Exception as e:
                print("Failed to forward to PI:", e)
    except Exception as e:
        print("Parse error:", e)

    return "OK", 200

if __name__ == "__main__":
    app.run()
