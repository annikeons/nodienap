from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import random
import os

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)

# Cargar intents desde la carpeta models
intents = json.load(open('models/intents.json', encoding='utf-8'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/alarms')
def alarms():
    return render_template('alarms.html')

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

@app.route('/ayuda')
def ayuda():
    return render_template('ayuda.html')

@app.route('/service-worker.js')
def service_worker():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'service-worker.js',
        mimetype='application/javascript'
    )

# Función de similitud simple
def similar_text(s1, s2):
    w1 = s1.split()
    w2 = s2.split()
    if not w1 or not w2:
        return 0.0
    return sum(1 for word in w1 if word in w2) / max(len(w1), len(w2))

def predict_intent(message):
    if not message:
        return "default"
    
    message = message.lower().strip()

    for intent in intents.get("intents", []):
        for pattern in intent.get("patterns", []):
            if pattern.lower() in message:
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


if __name__ == '__main__':
    app.run(debug=True, port=5000)
