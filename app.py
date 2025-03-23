@app.route("/sms", methods=["POST"])
def sms_reply():
    incoming_msg = request.form.get("Body", "")
    user_number = request.form.get("From", "")

    try:
        payload = {
            "model": "openrouter/mistralai/mistral-7b-instruct",
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
        print("🔵 Full OpenRouter Response:", response_json)

        # Extract the response safely
        reply = response_json.get("choices", [{}])[0].get("message", {}).get("content", "Sorry, I couldn’t understand that.")

    except Exception as e:
        import traceback
        print("🔴 OpenRouter API Error:")
        traceback.print_exc()
        reply = f"Error: {str(e)}"

    twilio_response = MessagingResponse()
    twilio_response.message(reply)
    return str(twilio_response)








