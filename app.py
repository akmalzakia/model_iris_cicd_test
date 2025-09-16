# app.py
import joblib
import numpy as np
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load model
model = joblib.load("iris_rf_model.pkl")

@app.route("/")
def home():
    return "Iris Random Forest API is running!"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    features = np.array([[ 
        data["sepal_length"], 
        data["sepal_width"], 
        data["petal_length"], 
        data["petal_width"] 
    ]])
    
    prediction = model.predict(features)[0]
    return jsonify({"class": int(prediction)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)
