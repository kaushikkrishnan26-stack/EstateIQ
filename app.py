
from flask import Flask, render_template, request, jsonify
import numpy as np
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

# Sample training data
# Features: area, bedrooms, bathrooms, floors, age, location
X = np.array([
    [800, 2, 1, 1, 10, 1],
    [1000, 2, 2, 1, 5, 1],
    [1200, 3, 2, 1, 8, 2],
    [1500, 3, 2, 2, 4, 1],
    [1800, 4, 3, 2, 3, 1],
    [2000, 4, 3, 2, 2, 2],
    [900, 2, 1, 1, 15, 3],
    [1400, 3, 2, 1, 10, 2],
    [2200, 4, 3, 2, 1, 1],
    [2500, 5, 4, 3, 2, 1],
    [1100, 2, 2, 1, 12, 3],
    [1700, 3, 3, 2, 6, 2]
])

# Sample prices in Indian rupees
y = np.array([
    2500000, 3200000, 3800000, 5000000,
    6200000, 7000000, 2200000, 4200000,
    8500000, 10000000, 2800000, 5500000
])

# Train the machine learning model
model = LinearRegression()
model.fit(X, y)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return jsonify({"error": "Invalid request data."}), 400

        required = [
            "area", "bedrooms", "bathrooms",
            "floors", "age", "location"
        ]

        if any(key not in data for key in required):
            return jsonify({"error": "Please provide all property details."}), 400

        try:
            area = float(data["area"])
            bedrooms = int(data["bedrooms"])
            bathrooms = int(data["bathrooms"])
            floors = int(data["floors"])
            age = int(data["age"])
            location = int(data["location"])
        except (TypeError, ValueError, OverflowError):
            return jsonify({"error": "Please enter valid numeric values."}), 400

        if not np.isfinite(area):
            return jsonify({"error": "Area must be a valid number."}), 400

        if not 100 <= area <= 100000:
            return jsonify({"error": "Area must be between 100 and 100000."}), 400

        if not 1 <= bedrooms <= 20:
            return jsonify({"error": "Invalid number of bedrooms."}), 400

        if not 1 <= bathrooms <= 20:
            return jsonify({"error": "Invalid number of bathrooms."}), 400

        if not 1 <= floors <= 10:
            return jsonify({"error": "Invalid number of floors."}), 400

        if not 0 <= age <= 200:
            return jsonify({"error": "Invalid property age."}), 400

        if location not in [1, 2, 3]:
            return jsonify({"error": "Please select a valid location."}), 400

        features = np.array([[
            area, bedrooms, bathrooms,
            floors, age, location
        ]])

        prediction = float(model.predict(features)[0])
        prediction = max(0, prediction)

        return jsonify({
            "predicted_price": round(prediction, 2)
        })

    except Exception:
        app.logger.exception("Prediction error")
        return jsonify({
            "error": "An unexpected error occurred. Please try again."
        }), 500


if __name__ == "__main__":
    app.run(debug=False)