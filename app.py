@app.route("/sms", methods=["POST"])
def sms_reply():
    incoming_msg = request.form.get("Body", "")
    user_number = request.form.get("From", "")

    try:
        prompt = f"You are a wellness assistant. Help this user: {incoming_msg}"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "https://ai-wellness-chatbot.onrender.com",  # optional but recommended
            "X-Title": "AI Wellness Chatbot",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 200
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()  # trigger exception for bad status
        result = response.json()

        reply = result["choices"][0]["message"]["content"]

    except Exception as e:
        import traceback
        print("🔴 OpenRouter API Error:")
        traceback.print_exc()
        reply = f"Sorry, something went wrong: {str(e)}"

    twilio_response = MessagingResponse()
    twilio_response.message(reply)
    return str(twilio_response)







