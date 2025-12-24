from flask import Flask, jsonify
from flask_cors import CORS
import os
import sys

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Python Learning Platform is running!'}), 200

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Python Learning Platform API'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)
