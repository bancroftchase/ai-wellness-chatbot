from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import os
import requests

# Load environment variables
load_dotenv()

# Claude API key from .env
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

# ✅ Create Flask app BEFORE using @app.route
app = Flask(__name__)

@app.route("/")
def home():
    return "AI Wellness Chatbot is running!"

@app.route("/sms", methods=["POST"])
def sms_reply():
    incoming_msg = request.form.get("Body", "")
    user_number = request.form.get("From", "")

    try:
        headers = {
            "x-api-key": CLAUDE_API_KEY,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "claude-2",
            "max_tokens": 100,
            "temperature": 0.7,
            "messages": [
                {"role": "user", "content": f"You are a wellness assistant. Help this user: {incoming_msg}"}
            ]
        }

        response = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=payload)
        response.raise_for_status()
        reply = response.json()["content"]
    except Exception as e:
        print("Claude API Error:", e)
        reply = "Sorry, I had a problem responding."

    twilio_response = MessagingResponse()
    twilio_response.message(reply)
    return str(twilio_response)

if __name__ == "__main__":
    app.run(debug=True)



