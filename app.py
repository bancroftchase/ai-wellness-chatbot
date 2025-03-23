from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os
from dotenv import load_dotenv
import requests

# Load the API key from the .env file
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

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
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "https://ai-wellness-chatbot.onrender.com",
            "X-Title": "AI Wellness Chatbot",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "openchat/openchat-3.5-1210",
            "messages": [
                {"role": "system", "content": "You are a compassionate AI wellness assistant."},
                {"role": "user", "content": incoming_msg}
            ],
            "max_tokens": 200
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        data = response.json()

        # Check if the structure contains 'choices'
        if "choices" in data and data["choices"]:
            reply = data["choices"][0]["message"]["content"]
        else:
            reply = "Hmm... something unexpected happened in the response."

    except Exception as e:
        import traceback
        print("🔴 OpenRouter API Error:")
        traceback.print_exc()
        reply = f"Sorry, I had a problem responding: {str(e)}"

    twilio_response = MessagingResponse()
    twilio_response.message(reply)
    return str(twilio_response)








