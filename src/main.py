from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from
from lib_ml.preprocessing import preprocess_reviews
import requests
import os

app = Flask(__name__)
swagger = Swagger(app)

MODEL_PATH = os.getenv("MODEL_PATH", "model/sentiment_model.pkl")
MODEL_URL = os.getenv("MODEL_URL")

def download_model():
    """
    Download the model from MODEL_URL if it doesn't exist at MODEL_PATH. Saves the downloaded model to MODEL_PATH.
    """
    if not os.path.exists(MODEL_PATH):
        if not MODEL_URL:
            raise RuntimeError("MODEL_PATH does not exist and MODEL_URL is not set.")
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

        try:
            print(f"Downloading model from {MODEL_URL}...")
            response = requests.get(MODEL_URL)
            response.raise_for_status()

            with open(MODEL_PATH, "wb") as f:
                f.write(response.content)

            print("Model downloaded successfully.")
        except Exception as e:
            raise RuntimeError(f"Failed to download model: {e}")

download_model()
model = joblib.load(MODEL_PATH)

@app.route('/api/sentiment', methods=['POST'])
@swag_from("specs/predict.yml")
def predict():
    """Predict sentiment of the input text"""

    # Check if the request contains JSON data and the 'text' field is not empty
    data = request.get_json()
    if not data or 'text' not in data or not data['text'].strip():
        return jsonify({'error': 'Input text cannot be empty'}), 400
    
    try:
        # Preprocess the input text using the lib_ml library and predict sentiment using the loaded model
        preprocessed_data = preprocessing(data['text'])
        prediction = model.predict([preprocessed_data])[0]

        return jsonify({'sentiment': prediction}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/version', methods=['GET'])
@swag_from("specs/version.yml")
def version():
    model_version = os.getenv("MODEL_SERVICE_VERSION", "unknown")
    return jsonify({'model_service_version': model_version})

if __name__ == "__main__":

    # Defining the listening port and host of the model service through environment variables
    port = int(os.getenv("PORT", 8080)) 
    host = str(os.getenv("HOST", "0.0.0.0"))
    app.run(host=host, port=port)
