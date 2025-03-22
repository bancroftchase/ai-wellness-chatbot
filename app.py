from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os
from dotenv import load_dotenv
import requests

load_dotenv()
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

app = Flask(__name__)

@app.route("/")
def home():
    return "AI Wellness Chatbot is running!"

@app.route("/sms", methods=["POST"])
def sms_reply():
    incoming_msg = request.form.get("Body", "")
    twilio_response = MessagingResponse()

    try:
        headers = {
            "x-api-key": CLAUDE_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }

        payload = {
            "model": "claude-3-haiku-20240307",
            "max_tokens": 100,
            "temperature": 0.7,
            "messages": [
                {"role": "user", "content": f"You are a wellness assistant. Help this user: {incoming_msg}"}
            ]
        }

        response = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=payload)
        data = response.json()

        reply = data.get("content", [{"text": "No response"}])[0].get("text", "No reply found.")
    except Exception as e:
        print("Error:", e)
        reply = "Sorry, I had a problem responding."

    twilio_response.message(reply)
    return str(twilio_response)

if __name__ == "__main__":
    app.run(debug=True)