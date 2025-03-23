from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os
from dotenv import load_dotenv
import requests

# Load your API key from the .env file
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
        "HTTP-Referer": "https://ai-wellness-chatbot.onrender.com",  # required by OpenRouter
        "X-Title": "AI Wellness Chatbot"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",  # Or try another model like 'mistralai/mistral-7b-instruct'
        "messages": [
            {"role": "user", "content": incoming_msg}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        result = response.json()

        # OpenRouter returns the response in result['choices'][0]['message']['content']
        reply = result["choices"][0]["message"]["content"]

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








