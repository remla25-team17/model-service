from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from
from lib_ml.preprocessing import preprocess_text
import requests
import os
import joblib
import numpy as np

app = Flask(__name__)
swagger = Swagger(app)

MODEL_SERVICE_VERSION = os.getenv("MODEL_SERVICE_VERSION", "0.1.2")

MODEL_PATH = os.getenv("MODEL_PATH", "model/model.pkl")
MODEL_URL = os.getenv("MODEL_URL", "https://github.com/remla25-team17/model-training/releases/download/{MODEL_SERVICE_VERSION}/model.pkl").format(MODEL_SERVICE_VERSION=MODEL_SERVICE_VERSION)

BAG_OF_WORDS_PATH = os.getenv("BAG_OF_WORDS_PATH", "model/bag_of_words.pkl")
BAG_OF_WORDS_URL = os.getenv("BAG_OF_WORDS_URL", "https://github.com/remla25-team17/model-training/releases/download/{MODEL_SERVICE_VERSION}/bag_of_words.pkl").format(MODEL_SERVICE_VERSION=MODEL_SERVICE_VERSION)
        
def download(save_path, url):
    """
    Download a file from a given URL and save it to the specified path.
    
    Args:
        save_path (str): The path where the file will be saved.
        url (str): The URL to download the file from.
    """
    if not os.path.exists(save_path):
        if not url:
            raise RuntimeError("Path does not exist and URL is not set.")
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        try:
            print(f"Downloading from {url}...")
            response = requests.get(url)
            response.raise_for_status()

            with open(save_path, "wb") as f:
                f.write(response.content)

            print("Download was successful.")
        except Exception as e:
            raise RuntimeError(f"Failed to download: {e}")

# Download the model and bag of words if they do not exist
download(MODEL_PATH, MODEL_URL)
download(BAG_OF_WORDS_PATH, BAG_OF_WORDS_URL)
model = joblib.load(MODEL_PATH)
bag_of_words = joblib.load(BAG_OF_WORDS_PATH)

@app.route('/api/v1/sentiment', methods=['POST'])
@swag_from("specs/predict.yml")
def predict():
    """Predict sentiment of the input text"""
    
    # Check if the request contains JSON data and the 'text' field is not empty
    data = request.get_json()
    if not data or 'text' not in data or not data['text'].strip():
        return jsonify({'error': 'Input text cannot be empty'}), 400
    
    try:
        # Preprocess the input text using the lib_ml library and predict sentiment using the loaded model
        preprocessed_data = preprocess_text(data['text'])
        # Convert the preprocessed text to a numerical format using the bag of words model
        numerical_data = bag_of_words.transform([preprocessed_data]).toarray()
        # Use the loaded model to predict sentiment
        prediction = model.predict(numerical_data)
        # Convert the prediction to a list and extract the first element
        prediction = prediction.tolist()[0]

        return jsonify({'sentiment': prediction}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/version', methods=['GET'])
@swag_from("specs/version.yml")
def version():
    model_version = os.getenv("MODEL_SERVICE_VERSION", "unknown")
    return jsonify({'model_service_version': model_version})

if __name__ == "__main__":
    # Defining the listening port and host of the model service through environment variables
    port = int(os.getenv("PORT", 8080)) 
    host = os.getenv("HOST", "0.0.0.0")
    app.run(host=host, port=port)
