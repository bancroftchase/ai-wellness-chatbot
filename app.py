from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os
from dotenv import load_dotenv
import requests

# Load API key from .env
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

app = Flask(__name__)

@app.route("/")
def home():
    return "AI Wellness Chatbot is live!"

@app.route("/sms", methods=["POST"])
def sms_reply():
    incoming_msg = request.form.get("Body", "")
    user_number = request.form.get("From", "")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://ai-wellness-chatbot.onrender.com",
        "X-Title": "AI Wellness Chatbot"
    }

    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": incoming_msg}],
        "max_tokens": 300
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        result = response.json()

        # ✅ Safely access the content
        if "choices" in result and result["choices"]:
            reply = result["choices"][0]["message"]["content"]
        else:
            reply = "Hmm... something unexpected happened in the response."

    except Exception as e:
        import traceback
        print("🔴 OpenRouter API Error:")
        traceback.print_exc()
        reply = f"Error: {str(e)}"

    twilio_response = MessagingResponse()
    twilio_response.message(reply)
    return str(twilio_response)

if __name__ == "__main__":
    app.run(debug=True)








