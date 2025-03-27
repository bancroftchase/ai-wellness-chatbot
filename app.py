from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
<<<<<<< HEAD
import os
import requests
from dotenv import load_dotenv
from pathlib import Path

# Initialize Flask application
=======
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
>>>>>>> c11f12a62ecdf854551ee94b49e8e6359d345ee4
app = Flask(__name__)

# Load environment variables
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

# Configure API settings
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    raise RuntimeError("API key not found in environment variables")

# Application configuration
APP_CONFIG = {
    "railway_url": "https://your-app-name.up.railway.app",
    "api_endpoint": "https://openrouter.ai/api/v1/chat/completions",
    "model": "mistralai/mistral-7b-instruct",
    "timeout": 10
}

@app.route("/sms", methods=["POST"])
def handle_sms():
    """Process incoming SMS messages"""
    message = request.form.get("Body", "").strip()
    response = MessagingResponse()
    
    if not message:
        response.message("Please send a message to start chatting")
        return str(response)

    try:
<<<<<<< HEAD
=======
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
>>>>>>> c11f12a62ecdf854551ee94b49e8e6359d345ee4
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": APP_CONFIG["railway_url"],
            "X-Title": "AI Wellness Bot"
        }

<<<<<<< HEAD
        payload = {
            "model": APP_CONFIG["model"],
            "messages": [{"role": "user", "content": message}],
            "max_tokens": 200
        }

        api_response = requests.post(
            APP_CONFIG["api_endpoint"],
            headers=headers,
            json=payload,
            timeout=APP_CONFIG["timeout"]
        )
        api_response.raise_for_status()
        
        reply = api_response.json()["choices"][0]["message"]["content"]
=======
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
>>>>>>> c11f12a62ecdf854551ee94b49e8e6359d345ee4

    except requests.exceptions.RequestException as e:
        reply = f"API Error: {str(e)}"
    except Exception as e:
<<<<<<< HEAD
        reply = f"Unexpected Error: {str(e)}"

    response.message(reply)
    return str(response)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
=======
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
>>>>>>> c11f12a62ecdf854551ee94b49e8e6359d345ee4
