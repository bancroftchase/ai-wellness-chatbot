from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os
import requests
from dotenv import load_dotenv
import traceback
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Get API key from environment
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("No OPENAI_API_KEY found in environment variables")

logger.info("🔐 API Key loaded successfully")

# Your Railway URL (UPDATE THIS TO YOUR ACTUAL RAILWAY URL)
RAILWAY_URL = "https://your-app-name.up.railway.app"  # ⚠️ Change this!

@app.route("/sms", methods=["POST"])
def sms_reply():
    """Handle incoming SMS messages and respond using OpenRouter API"""
    incoming_msg = request.form.get("Body", "").strip()
    user_number = request.form.get("From", "")

    # Create Twilio response object early
    twilio_response = MessagingResponse()
    
    if not incoming_msg:
        twilio_response.message("Please send a message to start chatting.")
        return str(twilio_response)

    try:
        # Prepare payload for OpenRouter
        payload = {
            "model": "mistralai/mistral-7b-instruct",
            "messages": [{"role": "user", "content": incoming_msg}],
            "max_tokens": 200
        }

        # Prepare headers with YOUR Railway URL
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": RAILWAY_URL,
            "X-Title": "AI Wellness Chatbot"
        }

        # Send request to OpenRouter
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=10  # Add timeout to prevent hanging
        )
        response.raise_for_status()  # Raise exception for HTTP errors
        response_json = response.json()

        logger.debug("API Response: %s", response_json)

        # Extract response safely
        if "choices" in response_json and response_json["choices"]:
            reply = response_json["choices"][0]["message"]["content"]
        else:
            logger.error("Unexpected API response format: %s", response_json)
            reply = "I couldn't process that request. Please try again."

    except requests.exceptions.RequestException as e:
        logger.error("API request failed: %s", str(e))
        reply = "Sorry, I'm having trouble connecting to the service right now."
    except Exception as e:
        logger.error("Unexpected error: %s", traceback.format_exc())
        reply = "An unexpected error occurred. Please try again later."

    twilio_response.message(reply)
    return str(twilio_response)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=os.getenv("DEBUG", "false").lower() == "true")


