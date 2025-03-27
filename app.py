from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os
import requests
from dotenv import load_dotenv
from pathlib import Path

# Initialize Flask application
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
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": APP_CONFIG["railway_url"],
            "X-Title": "AI Wellness Bot"
        }

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

    except requests.exceptions.RequestException as e:
        reply = f"API Error: {str(e)}"
    except Exception as e:
        reply = f"Unexpected Error: {str(e)}"

    response.message(reply)
    return str(response)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)