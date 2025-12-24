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
        self.load_lessons_from_files()

    def init_database(self):
        """Initialize database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Lessons table (metadata)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lessons (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                order_num INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # User progress table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lesson_id TEXT NOT NULL,
                exercise_id TEXT,
                completed BOOLEAN DEFAULT FALSE,
                last_code TEXT,
                test_passed BOOLEAN DEFAULT FALSE,
                completed_at TIMESTAMP,
                FOREIGN KEY (lesson_id) REFERENCES lessons(id)
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
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (lesson_id) REFERENCES lessons(id)
            )
        ''')

        conn.commit()
        conn.close()

    def load_lessons_from_files(self):
        """Load all lesson files and insert into database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if not os.path.exists(self.lessons_dir):
            os.makedirs(self.lessons_dir, exist_ok=True)

        lesson_files = sorted([f for f in os.listdir(self.lessons_dir) if f.endswith('.json')])

        for file in lesson_files:
            try:
                with open(os.path.join(self.lessons_dir, file), 'r', encoding='utf-8') as f:
                    lesson_data = json.load(f)

                    # Check if lesson already exists
                    cursor.execute('SELECT id FROM lessons WHERE id = ?', (lesson_data.get('id'),))
                    if not cursor.fetchone():
                        cursor.execute('''
                            INSERT INTO lessons (id, title, order_num)
                            VALUES (?, ?, ?)
                        ''', (
                            lesson_data.get('id'),
                            lesson_data.get('title'),
                            lesson_data.get('order', 0)
                        ))
            except Exception as e:
                print(f"Error loading lesson file {file}: {e}")

        conn.commit()
        conn.close()

    def get_all_lessons(self):
        """Get list of all lessons"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, title, order_num FROM lessons ORDER BY order_num
        ''')

        lessons = []
        for row in cursor.fetchall():
            # Get full lesson data from JSON file to get description and week
            lesson_file = os.path.join(self.lessons_dir, f'{row[0]}.json')
            description = ''
            week = 0
            try:
                if os.path.exists(lesson_file):
                    with open(lesson_file, 'r', encoding='utf-8') as f:
                        lesson_json = json.load(f)
                        description = lesson_json.get('description', '')
                        week = lesson_json.get('week', 0)
            except:
                pass

            lessons.append({
                'id': row[0],
                'title': row[1],
                'order': row[2],
                'description': description,
                'week': week
            })

        conn.close()
        return lessons

    def get_lesson(self, lesson_id):
        """Get a specific lesson with full content"""
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
        """Get lesson metadata from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, title, order_num FROM lessons WHERE id = ?
        ''', (lesson_id,))

        row = cursor.fetchone()
        conn.close()

        if row:
            # Get full lesson data from JSON file
            lesson_file = os.path.join(self.lessons_dir, f'{lesson_id}.json')
            description = ''
            week = 0
            try:
                if os.path.exists(lesson_file):
                    with open(lesson_file, 'r', encoding='utf-8') as f:
                        lesson_json = json.load(f)
                        description = lesson_json.get('description', '')
                        week = lesson_json.get('week', 0)
            except:
                pass

            return {
                'id': row[0],
                'title': row[1],
                'order': row[2],
                'description': description,
                'week': week
            }

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
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Total lessons
        cursor.execute('SELECT COUNT(*) FROM lessons')
        total = cursor.fetchone()[0]

        # Completed lessons
        cursor.execute('SELECT COUNT(DISTINCT lesson_id) FROM user_progress WHERE completed = TRUE')
        completed = cursor.fetchone()[0]

        # Current lesson (next incomplete)
        cursor.execute('''
            SELECT id FROM lessons
            WHERE id NOT IN (SELECT lesson_id FROM user_progress WHERE completed = TRUE)
            ORDER BY order_num LIMIT 1
        ''')
        current = cursor.fetchone()

        conn.close()

        return {
            'total': total,
            'completed': completed,
            'current_lesson_id': current[0] if current else None,
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
