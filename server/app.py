import os
import joblib
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model/basic_model.pkl")
model = None

def load_model():
    global model
    if os.path.exists(MODEL_PATH):
        print("Loading model...")
        model = joblib.load(MODEL_PATH)
        print("Model loaded.")
    else:
        print("Model not found! Please run train_model.py first.")

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Fake Job Detector API is running", "model_loaded": model is not None})

@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({"error": "Model not loaded"}), 500
    
    data = request.json
    text = data.get('text', '')
    
    if not text:
        # Try to construct from fields if 'text' not explicitly provided
        title = data.get('title', '')
        description = data.get('description', '')
        company = data.get('company_profile', '')
        requirements = data.get('requirements', '')
        benefits = data.get('benefits', '')
        
        text = f"{title} {company} {description} {requirements} {benefits}".strip()
    
    if not text:
        return jsonify({"error": "No text provided"}), 400
    
    # Predict
    # The pipeline handles vectorization
    prediction = model.predict([text])[0]
    probabilities = model.predict_proba([text])[0]
    
    # Probability of class 1 (Fraudulent)
    fraud_prob = probabilities[1]
    
    return jsonify({
        "trust_score": round((1 - fraud_prob) * 100, 2),
        "is_fraud": bool(prediction == 1),
        "fraud_probability": float(fraud_prob)
    })

if __name__ == '__main__':
    load_model()
    app.run(debug=True, port=5000)
