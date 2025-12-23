# Importación de bibliotecas
from flask import Flask, render_template, request, jsonify
import json
import random
from flask_cors import CORS  # Importa la extensión CORS
 
app = Flask(__name__)
app.static_folder = 'static'

CORS(app)  # Habilita CORS en la aplicación Flask
app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)


# Declarar intents de manera global
intents = json.load(open('chat_bot/intents.json', encoding='utf-8'))

# Función para calcular la similitud entre dos cadenas de texto
def similar_text(s1, s2):
    return sum(1 for word in s1.split() if word in s2.split()) / max(len(s1.split()), len(s2.split()))

# Función para predecir la intención del mensaje del usuario
def predict_intent(message):
    message = message.lower()
    max_sim = 0
    best_match_index = -1

    for i, intent in enumerate(intents['intents']):
        for pattern in intent['patterns']:
            pattern = pattern.lower()
            similarity = similar_text(message, pattern)
            if similarity > max_sim:
                max_sim = similarity
                best_match_index = i

    if best_match_index != -1:
        predicted_intent = intents['intents'][best_match_index]['tag']
    else:
        predicted_intent = "intencion_desconocida"

    return predicted_intent

# Función para obtener una respuesta basada en la intención
def get_response(intent):
    for item in intents['intents']:
        if 'tag' in item and item['tag'] == intent:
            responses = item['responses']
            response = random.choice(responses)
            if isinstance(response, dict):
                # Respuesta con imagen o enlace
                return response
            else:
                # Respuesta de texto normal
                return response

    return "No estoy seguro de entender. ¿Puedes reformular tu pregunta?"

# Ruta para cargar la página de chat y las intenciones del chatbot
@app.route('/chat', methods=['GET'])
def chat():
    return render_template('index.html', intents=intents)

# Ruta de inicio para renderizar una plantilla HTML
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para la página principal
@app.route('/principal')
def principal():
    return render_template('mainx')

# ...


# Ruta para obtener respuestas del bot a través de una solicitud POST
@app.route('/get_response', methods=['POST'])
def get_bot_response():
    user_message = request.form['user_message']
    intent = predict_intent(user_message)
    bot_response = get_response(intent)

    if isinstance(bot_response, dict):
        # Respuesta con imagen o enlace
        response_text = bot_response.get('text', '')
        image_url = bot_response.get('image_url', '')  # Acceder a la URL de la imagen
        link_url = bot_response.get('link_url', '')  # Acceder a la URL del enlace
        return jsonify({'user_response': user_message, 'bot_response': response_text, 'bot_response_image': image_url, 'bot_response_link': link_url})
    else:
        # Respuesta de texto normal
        return jsonify({'user_response': user_message, 'bot_response': bot_response})

# Iniciar la aplicación Flask si se ejecuta este archivo directamente
if __name__ == '__main__':
    app.run(debug=True)
