from flask import Flask, jsonify
from flask_cors import CORS
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Python Learning Platform is running!'}), 200

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Python Learning Platform API', 'version': '1.0'}), 200

@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({'test': 'success'}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)
