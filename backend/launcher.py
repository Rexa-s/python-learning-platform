#!/usr/bin/env python
"""
Launcher for Python Learning Platform
This file is used to start the application
"""

import sys
import os
import webbrowser
import time
from pathlib import Path

# Add the backend directory to the path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

# Set environment variables
os.environ['FLASK_ENV'] = 'production'

def main():
    """Start the application"""
    try:
        print(f"Python path: {sys.path}")
        print(f"Backend dir: {backend_dir}")
        print("Importing app...")

        # Import after adding to path
        from app import app
        from waitress import serve

        port = int(os.environ.get('PORT', 5001))
        host = '0.0.0.0'

        print("=" * 60)
        print("🐍 Python Öğrenme Platformu")
        print("=" * 60)
        print(f"\n✓ Sunucu başlatılıyor...")
        print(f"✓ Adres: http://0.0.0.0:{port}")
        print(f"\nÇıkmak için: Ctrl+C basın\n")

        # Wait a moment then open browser (only if not on Render)
        if 'RENDER' not in os.environ:
            def open_browser():
                time.sleep(2)
                try:
                    webbrowser.open(f'http://localhost:{port}')
                except:
                    pass

            # Start browser opening in background
            import threading
            browser_thread = threading.Thread(target=open_browser, daemon=True)
            browser_thread.start()

        # Start server
        print(f"Waitress serveri başlatılıyor...\n")
        serve(app, host=host, port=port, _quiet=False)

    except Exception as e:
        import traceback
        print(f"\n❌ Hata oluştu: {e}")
        print(f"\nTraceback:")
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
