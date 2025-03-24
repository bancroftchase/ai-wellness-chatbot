from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

app = Flask(__name__)

@app.route("/sms", methods=["POST"])
def sms_reply():
    incoming_msg = request.form.get("Body", "")
    user_number = request.form.get("From", "")

    try:
        payload = {
    "model": "openrouter/openai/gpt-3.5-turbo",
    "messages": [
        {"role": "user", "content": incoming_msg}
    ],
    "max_tokens": 200
}

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://ai-wellness-chatbot.onrender.com",
            "X-Title": "AI Wellness Chatbot"
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        response_json = response.json()
        print("🔵 FULL API RESPONSE:\n", response_json)

        if "choices" in response_json and response_json["choices"]:
            reply = response_json["choices"][0]["message"]["content"]
        else:
            print("⚠️ 'choices' missing or empty in response!")
            reply = "Hmm... something unexpected happened in the response."

    except Exception as e:
        import traceback
        print("🔴 Exception occurred:")
        traceback.print_exc()
        reply = f"Error: {str(e)}"

    twilio_response = MessagingResponse()
    twilio_response.message(reply)
    return str(twilio_response)







