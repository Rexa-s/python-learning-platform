from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import sys

# Add backend to path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from database.db import Database
from services.code_executor import CodeExecutor

# Initialize Flask app with frontend static files
app = Flask(__name__,
            static_folder='../frontend',
            static_url_path='/')
CORS(app)

# Initialize database and executor
db = Database()
executor = CodeExecutor(timeout=5, max_output=10000)

# ==================== HEALTH CHECK ====================
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Python Learning Platform is running!'}), 200

@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({'test': 'success'}), 200

# ==================== LESSONS ====================
@app.route('/api/lessons', methods=['GET'])
def get_lessons():
    """Get list of all lessons"""
    try:
        lessons = db.get_all_lessons()
        progress = db.get_progress()
        return jsonify({
            'success': True,
            'lessons': lessons,
            'progress': progress
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/lessons/<lesson_id>', methods=['GET'])
def get_lesson(lesson_id):
    """Get a specific lesson with full content"""
    try:
        lesson = db.get_lesson(lesson_id)
        if not lesson:
            return jsonify({'success': False, 'error': 'Lesson not found'}), 404

        # Get progress for this lesson
        lesson_progress = db.get_lesson_progress(lesson_id)

        return jsonify({
            'success': True,
            'lesson': lesson,
            'progress': lesson_progress
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/lessons/<lesson_id>/complete', methods=['POST'])
def complete_lesson(lesson_id):
    """Mark a lesson as completed"""
    try:
        db.mark_lesson_complete(lesson_id)
        progress = db.get_progress()
        return jsonify({
            'success': True,
            'progress': progress
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== CODE EXECUTION ====================
@app.route('/api/execute', methods=['POST'])
def execute_code():
    """Execute Python code"""
    try:
        data = request.get_json()
        code = data.get('code', '')
        lesson_id = data.get('lesson_id', '')
        exercise_id = data.get('exercise_id', '')

        if not code:
            return jsonify({'success': False, 'error': 'No code provided'}), 400

        # Execute code
        result = executor.execute(code)

        # Save submission
        if lesson_id and exercise_id:
            db.save_code_submission(
                lesson_id,
                exercise_id,
                code,
                result.get('output', ''),
                result.get('success', False)
            )

        return jsonify({
            'success': True,
            'execution': result
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/exercises/<exercise_id>/test', methods=['POST'])
def test_exercise(exercise_id):
    """Run code against test cases"""
    try:
        data = request.get_json()
        code = data.get('code', '')
        test_cases = data.get('test_cases', [])
        lesson_id = data.get('lesson_id', '')

        if not code:
            return jsonify({'success': False, 'error': 'No code provided'}), 400

        # Run tests
        test_result = executor.run_tests(code, test_cases)

        # If all tests pass, mark exercise as complete
        if test_result['success'] and lesson_id:
            db.mark_exercise_complete(lesson_id, exercise_id)

        return jsonify({
            'success': True,
            'test_result': test_result
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== PROGRESS ====================
@app.route('/api/progress', methods=['GET'])
def get_progress():
    """Get user progress"""
    try:
        progress = db.get_progress()
        return jsonify({
            'success': True,
            'progress': progress
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== FRONTEND SERVING ====================
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
