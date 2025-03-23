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








