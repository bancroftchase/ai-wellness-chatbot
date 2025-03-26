from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os
import requests
from dotenv import load_dotenv
import traceback

# Initialize the Flask application
app = Flask(__name__)

# Load environment variables
load_dotenv()

# Configure API settings
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("API key not found in environment variables")

# Application configuration
APP_CONFIG = {
    "railway_url": "https://your-app-name.up.railway.app",  # UPDATE THIS
    "api_endpoint": "https://openrouter.ai/api/v1/chat/completions",
    "model": "mistralai/mistral-7b-instruct",
    "timeout": 10
}

@app.route("/sms", methods=["POST"])
def handle_sms():
    """Process incoming SMS messages"""
    message = request.form.get("Body", "").strip()
    sender = request.form.get("From", "")
    
    response = MessagingResponse()
    
    if not message:
        response.message("Please send a message to start chatting")
        return str(response)

    try:
        # Prepare API request
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

        # Make API call
        api_response = requests.post(
            APP_CONFIG["api_endpoint"],
            headers=headers,
            json=payload,
            timeout=APP_CONFIG["timeout"]
        )
        api_response.raise_for_status()
        
        # Process response
        response_data = api_response.json()
        if response_data.get("choices"):
            reply = response_data["choices"][0]["message"]["content"]
        else:
            reply = "I couldn't process your request. Please try again."

    except requests.exceptions.RequestException:
        reply = "Service temporarily unavailable. Please try later."
    except Exception:
        reply = "An internal error occurred. Please try again."

    response.message(reply)
    return str(response)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)