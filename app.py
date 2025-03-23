from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os
import requests
from dotenv import load_dotenv

load_dotenv()
claude_api_key = os.getenv("CLAUDE_API_KEY")

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
            "x-api-key": claude_api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }

        data = {
            "model": "claude-2.1",
            "max_tokens": 300,
            "temperature": 0.6,
            "messages": [
                {
                    "role": "user",
                    "content": f"You are a helpful wellness assistant. Help this person with their question: {incoming_msg}"
                }
            ]
        }

        response = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=data)
        result = response.json()
        reply = result.get("content", [{"text": "Sorry, I had a problem responding."}])[0]["text"]

    except Exception as e:
        reply = "Sorry, I had a problem responding."

    twilio_response = MessagingResponse()
    twilio_response.message(reply)
    return str(twilio_response)

if __name__ == "__main__":
    app.run(debug=True)
