from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Serve your main page
@app.route("/")
def home():
    return render_template("UI.html")

# Simple API endpoint for the chat (you can replace this with real AI later)
@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    # For now, just echo back something simple
    fake_reply = f"You said: {user_message}. (This is where AI will reply later 🤖)"

    return jsonify({"reply": fake_reply})

if __name__ == "__main__":
    app.run(debug=True)
