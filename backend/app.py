from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def home():
    return jsonify({'message': 'Hello from Flask backend!'})

@app.route('/api/data')
def get_data():
    return jsonify({'message': 'This is a response from the backend!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)  # Ensure the app runs on port 8080

