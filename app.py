from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from chatbot import EnvironmentalChatbot


app = Flask(__name__)
CORS(app)

chatbot = EnvironmentalChatbot()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "Darukaa Earth Environmental Intelligence API"
    })


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()

        soil_carbon = float(data.get("soil_carbon", 0))
        rainfall = float(data.get("rainfall", 0))
        land_use = data.get("land_use", "monoculture")
        region = data.get("region", "")

        result = chatbot.analyze(
            soil_carbon=soil_carbon,
            rainfall=rainfall,
            land_use=land_use,
            region=region
        )

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400


@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json()

        result = chatbot.analyze(
            soil_carbon=float(data["soil_carbon"]),
            rainfall=float(data["rainfall"]),
            land_use=data["land_use"],
            region=data.get("region", "")
        )

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400


if __name__ == "__main__":
    app.run(debug=True)