from flask import Flask, request
import openai
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "AI Wellness Chatbot is running!"

if __name__ == "__main__":
    app.run(debug=True)