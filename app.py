from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
import random

app = Flask(__name__)
CORS(app)

# Cargar intents desde la carpeta models
intents = json.load(open('models/intents.json', encoding='utf-8'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

# Función de similitud simple
def similar_text(s1, s2):
    return sum(1 for word in s1.split() if word in s2.split()) / max(len(s1.split()), len(s2.split()))

def predict_intent(message):
    message = message.lower()

    for intent in intents["intents"]:
        for pattern in intent["patterns"]:
            if pattern in message:
                return intent["tag"]

    return "default"


def get_response(intent):
    for item in intents['intents']:
        if item['tag'] == intent:
            return random.choice(item['responses'])
    return "No estoy segura de entenderte 🤍"

@app.route('/get_response', methods=['POST'])
def get_bot_response():
    user_message = request.form.get('user_message')
    intent = predict_intent(user_message)
    bot_response = get_response(intent)

    return jsonify({
        'bot_response': bot_response
    })
