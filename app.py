from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Get the bot token from environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not set in environment variables")

# Telegram API URL for sending messages
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

@app.route("/", methods=["GET"])
def index():
    return "Backend is running!"

@app.route("/send-message", methods=["POST"])
def send_message():
    # Get chat_id and text from the POST form data
    chat_id = request.form.get("chat_id")
    text = request.form.get("text")

    # Validate input
    if not chat_id or not text:
        return jsonify({"error": "chat_id and text are required"}), 400

    # Send message to Telegram Bot API
    response = requests.post(TELEGRAM_API_URL, data={
        "chat_id": chat_id,
        "text": text
    })

    # Check Telegram response status
    if response.status_code == 200:
        return jsonify({"success": True}), 200
    else:
        # Return Telegram API error
        return jsonify({"error": response.text}), 500

if __name__ == "__main__":
    # Run the Flask development server
    app.run(debug=True)
