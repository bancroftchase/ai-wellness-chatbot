from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "AI Wellness Chatbot is running!"

if __name__ == '__main__':
    app.run(debug=True)
