from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from chatbot import BiodiversityChatbot
import traceback
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

try:
    bot = BiodiversityChatbot()
    print("✓ Chatbot initialized successfully")
except Exception as e:
    print(f"ERROR initializing chatbot: {e}")
    bot = None


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():

    try:

        if not bot:
            return jsonify({
                "error": "Chatbot not initialized. Check OpenAI API key."
            }), 500

        data = request.json

        if not data:
            return jsonify({
                "error": "No input provided"
            }), 400

        input_text = f"""
        Soil carbon: {data.get('soil_carbon', 'N/A')}%
        Rainfall: {data.get('rainfall', 'N/A')}mm
        Land use: {data.get('land_use', 'N/A')}
        Region: {data.get('region', 'N/A')}
        """

        response = bot.process_input(input_text)

        return jsonify({
            "status": "success",
            "response": response
        }), 200

    except Exception as e:

        return jsonify({
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500


@app.route('/chat', methods=['POST'])
def chat():

    try:

        if not bot:
            return jsonify({
                "error": "Chatbot not initialized"
            }), 500

        data = request.json

        user_message = data.get(
            'message',
            ''
        )

        if not user_message:

            return jsonify({
                "error": "No message provided"
            }), 400

        response = bot.process_input(
            user_message
        )

        return jsonify({
            "status": "success",
            "response": response
        }), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


@app.route('/health')
def health():

    return jsonify({
        "status": "System running",
        "bot_initialized": bot is not None
    }), 200


if __name__ == '__main__':

    print("\n" + "=" * 80)
    print("STARTING DARUKAA.EARTH BIODIVERSITY CHATBOT API")
    print("=" * 80)

    print("\nAvailable Endpoints:")
    print("  GET  http://localhost:5000/")
    print("  GET  http://localhost:5000/dashboard")
    print("  GET  http://localhost:5000/health")
    print("  POST http://localhost:5000/analyze")
    print("  POST http://localhost:5000/chat")

    print("\nPress Ctrl+C to stop server\n")

    app.run(
        debug=True,
        port=5000,
        use_reloader=False
    )