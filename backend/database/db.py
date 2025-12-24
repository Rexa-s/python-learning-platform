import json
import os
import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_path=None):
        # Get the directory of the current file and work from there
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)  # backend directory

        if db_path is None:
            db_path = os.path.join(parent_dir, 'database', 'learning.db')

        self.db_path = db_path
        self.lessons_dir = os.path.join(parent_dir, 'data', 'lessons')

        # Ensure directories exist
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        os.makedirs(self.lessons_dir, exist_ok=True)

        self.init_database()

    def init_database(self):
        """Initialize database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # User progress table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lesson_id TEXT NOT NULL,
                exercise_id TEXT,
                completed BOOLEAN DEFAULT FALSE,
                last_code TEXT,
                test_passed BOOLEAN DEFAULT FALSE,
                completed_at TIMESTAMP
            )
        ''')

        # Code submissions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS code_submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                exercise_id TEXT NOT NULL,
                lesson_id TEXT NOT NULL,
                code TEXT NOT NULL,
                output TEXT,
                success BOOLEAN,
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        conn.close()

    def get_all_lessons(self):
        """Get list of all lessons from JSON files"""
        lessons = []

        if not os.path.exists(self.lessons_dir):
            return lessons

        # Load all lesson JSON files
        lesson_files = sorted([f for f in os.listdir(self.lessons_dir) if f.endswith('.json')])

        for filename in lesson_files:
            lesson_file = os.path.join(self.lessons_dir, filename)
            try:
                with open(lesson_file, 'r', encoding='utf-8') as f:
                    lesson_json = json.load(f)
                    lessons.append({
                        'id': lesson_json.get('id'),
                        'title': lesson_json.get('title'),
                        'order': lesson_json.get('order', 0),
                        'description': lesson_json.get('description', ''),
                        'week': lesson_json.get('week', 0)
                    })
            except Exception as e:
                print(f"Error loading lesson file {filename}: {e}")

        # Sort by order
        lessons.sort(key=lambda x: x['order'])
        return lessons

    def get_lesson(self, lesson_id):
        """Get a specific lesson with full content from JSON file"""
        lesson_file = os.path.join(self.lessons_dir, f'{lesson_id}.json')

        if os.path.exists(lesson_file):
            try:
                with open(lesson_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading lesson {lesson_id}: {e}")
                return None

        return None

    def get_lesson_metadata(self, lesson_id):
        """Get lesson metadata from JSON file"""
        lesson_file = os.path.join(self.lessons_dir, f'{lesson_id}.json')

        if os.path.exists(lesson_file):
            try:
                with open(lesson_file, 'r', encoding='utf-8') as f:
                    lesson_json = json.load(f)
                    return {
                        'id': lesson_json.get('id'),
                        'title': lesson_json.get('title'),
                        'order': lesson_json.get('order'),
                        'description': lesson_json.get('description', ''),
                        'week': lesson_json.get('week', 0)
                    }
            except Exception as e:
                print(f"Error loading lesson metadata {lesson_id}: {e}")

        return None

    def mark_lesson_complete(self, lesson_id):
        """Mark a lesson as completed"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT OR REPLACE INTO user_progress (lesson_id, completed, completed_at)
            VALUES (?, TRUE, ?)
        ''', (lesson_id, datetime.now().isoformat()))

        conn.commit()
        conn.close()

    def mark_exercise_complete(self, lesson_id, exercise_id):
        """Mark an exercise as completed"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT OR REPLACE INTO user_progress (lesson_id, exercise_id, test_passed, completed_at)
            VALUES (?, ?, TRUE, ?)
        ''', (lesson_id, exercise_id, datetime.now().isoformat()))

        conn.commit()
        conn.close()

    def save_code_submission(self, lesson_id, exercise_id, code, output, success):
        """Save code submission for an exercise"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO code_submissions (lesson_id, exercise_id, code, output, success)
            VALUES (?, ?, ?, ?, ?)
        ''', (lesson_id, exercise_id, code, output, success))

        conn.commit()
        conn.close()

    def get_progress(self):
        """Get overall user progress"""
        lessons = self.get_all_lessons()
        total = len(lessons)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Completed lessons
        cursor.execute('SELECT COUNT(DISTINCT lesson_id) FROM user_progress WHERE completed = TRUE')
        completed = cursor.fetchone()[0]

        # Current lesson (next incomplete)
        cursor.execute('''
            SELECT lesson_id FROM user_progress WHERE completed = TRUE ORDER BY completed_at DESC LIMIT 1
        ''')
        current_result = cursor.fetchone()
        current_lesson_id = None
        if current_result:
            # Get next lesson
            current_id = current_result[0]
            for lesson in lessons:
                if lesson['id'] == current_id:
                    idx = lessons.index(lesson)
                    if idx + 1 < len(lessons):
                        current_lesson_id = lessons[idx + 1]['id']
                    break
        else:
            # No lessons completed, start with first
            if lessons:
                current_lesson_id = lessons[0]['id']

        conn.close()

        return {
            'total': total,
            'completed': completed,
            'current_lesson_id': current_lesson_id,
            'percentage': (completed / total * 100) if total > 0 else 0
        }

    def get_lesson_progress(self, lesson_id):
        """Get progress for a specific lesson"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT COUNT(*) FROM user_progress
            WHERE lesson_id = ? AND test_passed = TRUE
        ''', (lesson_id,))

        passed_exercises = cursor.fetchone()[0]

        conn.close()

        return {
            'lesson_id': lesson_id,
            'passed_exercises': passed_exercises
        }
