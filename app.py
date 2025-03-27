from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
<<<<<<< HEAD
import os
from dotenv import load_dotenv
import requests

# Load the API key from the .env file
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

=======
import request

from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
print(f"🔐 Loaded API Key: {api_key}")
Initialize Flask app
>>>>>>> dbb90e25c7ab7621468ec0389203f0799371fc24
app = Flask(__name__)

@app.route("/sms", methods=["POST"])
def sms_reply():
    incoming_msg = request.form.get("Body", "")
    user_number = request.form.get("From", "")

    try:
<<<<<<< HEAD
        # OpenRouter API headers
=======
        Prepare payload for OpenRouter
        payload = {
            "model": "mistralai/mistral-7b-instruct",
            "messages": [
                {"role": "user", "content": incoming_msg}
            ],
            "max_tokens": 200
        }

        Prepare headers as required by OpenRouter
>>>>>>> dbb90e25c7ab7621468ec0389203f0799371fc24
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://ai-wellness-chatbot.onrender.com",
            "X-Title": "AI Wellness Chatbot"
        }

<<<<<<< HEAD
        # OpenRouter API payload
        payload = {
            "model": "openrouter/mistralai/mistral-7b-instruct",
            "messages": [
                {"role": "user", "content": incoming_msg}
            ],
            "max_tokens": 200
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        response_json = response.json()

        print("🔵 Full OpenRouter Response:", response_json)

        # Safely extract assistant message
        if "choices" in response_json:
            reply = response_json["choices"][0]["message"]["content"]
        else:
=======
        Send request to OpenRouter
        
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        response_json = response.json()
        print("🔵 FULL API RESPONSE:", response_json)
        print("🚀 Making API call with headers:", headers)
        print("📦 Payload:", payload)
        Extract response safely
        if "choices" in response_json and response_json["choices"]:
            reply = response_json["choices"][0]["message"]["content"]
        else:
            print("⚠️ 'choices' missing or empty in response!")
>>>>>>> dbb90e25c7ab7621468ec0389203f0799371fc24
            reply = "Hmm... something unexpected happened in the response."

    except Exception as e:
        import traceback
<<<<<<< HEAD
        print("🔴 OpenRouter API Error:")
        traceback.print_exc()
        reply = f"Error: {str(e)}"

    # Create Twilio response
=======
        print("🔴 Exception occurred:")
        traceback.print_exc()
        reply = f"Error: {str(e)}"

    Create Twilio response
>>>>>>> dbb90e25c7ab7621468ec0389203f0799371fc24
    twilio_response = MessagingResponse()
    twilio_response.message(reply)
    return str(twilio_response)

<<<<<<< HEAD
if __name__ == "__main__":
    app.run(debug=True)
=======
Only for local testing (ignored by Render)
if __name__ == "__main__":
    app.run(debug=True)









>>>>>>> dbb90e25c7ab7621468ec0389203f0799371fc24
