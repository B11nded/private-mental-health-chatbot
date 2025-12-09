from flask import Flask, render_template, request, jsonify
from AI import respond

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("UI.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "No message provided."}), 400
    
    bot_reply = respond(user_message)

    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)
