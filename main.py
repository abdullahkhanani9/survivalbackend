# import "packages" from flask
from flask import Flask, jsonify, request
from flask_cors import CORS

# import "packages" from "this" project
from sklearn.preprocessing import OneHotEncoder
import pandas as pd

# setup Flask App
app = Flask(__name__)
CORS(app)

# Encode categorical variables
enc = OneHotEncoder(handle_unknown='ignore')

# Preprocess the data
def preprocess_data(passenger_data):
    # Convert data to DataFrame
    passenger_df = pd.DataFrame(passenger_data)

    # Encode 'sex' variable
    passenger_df['sex'] = passenger_df['sex'].apply(lambda x: 1 if x == 'male' else 0)

    # Encode 'alone' variable
    passenger_df['alone'] = passenger_df['alone'].apply(lambda x: 1 if x else 0)

    # Encode 'embarked' variable
    onehot = enc.transform(passenger_df[['embarked']]).toarray()
    cols = ['embarked_' + val for val in enc.categories_[0]]
    passenger_df[cols] = pd.DataFrame(onehot)

    # Drop unnecessary columns
    passenger_df.drop(['name', 'embarked'], axis=1, inplace=True)

    return passenger_df

# Load the machine learning model
# Replace this with your model loading code
# For demonstration purposes, using a placeholder
def load_model():
    pass

# Make predictions using the loaded model
def predict_survival(passenger_data):
    # Preprocess the data
    passenger_df = preprocess_data(passenger_data)

    # Load the model
    model = load_model()  # Load your machine learning model here

    # Make predictions
    # For demonstration purposes, returning placeholder results
    return {'Survival probability': 0.75}

# Define endpoint for prediction
@app.route('/api/titanic/predict', methods=['POST'])
def predict():
    try:
        # Get data from request
        passenger_data = request.json

        # Make predictions
        result = predict_survival(passenger_data)

        # Return predictions
        return jsonify(result), 200
    except Exception as e:
        # Return error message
        return jsonify({'error': str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=8086)
