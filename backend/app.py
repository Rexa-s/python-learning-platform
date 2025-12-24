from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os

# Initialize Flask app with frontend static files
app = Flask(__name__,
            static_folder='../frontend',
            static_url_path='/')
CORS(app)

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Python Learning Platform is running!'}), 200

@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({'test': 'success'}), 200

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    """Serve frontend files, fallback to index.html for SPA"""
    # Don't serve /api/* routes here
    if path.startswith('api/'):
        return jsonify({'error': 'Not found'}), 404

    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)
