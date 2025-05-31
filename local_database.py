import sqlite3
import json
from datetime import datetime
import os

class LocalDatabase:
    def __init__(self):
        self.db_path = 'browser_data.db'
        self.initialize_database()

    def initialize_database(self):
        """Initialize the SQLite database with required tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Create bookmarks table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS bookmarks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    url TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Create history table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT NOT NULL,
                    title TEXT,
                    visited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Create settings table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                )
            ''')

            # Create downloads table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS downloads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    url TEXT NOT NULL,
                    path TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error initializing database: {str(e)}")
            return False

    def add_bookmark(self, title, url):
        """Add a new bookmark"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO bookmarks (title, url) VALUES (?, ?)",
                (title, url)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error adding bookmark: {str(e)}")
            return False

    def get_bookmarks(self):
        """Get all bookmarks"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM bookmarks ORDER BY created_at DESC")
            bookmarks = cursor.fetchall()
            conn.close()
            return bookmarks
        except Exception as e:
            print(f"Error getting bookmarks: {str(e)}")
            return []

    def add_history(self, url, title):
        """Add a new history entry"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO history (url, title) VALUES (?, ?)",
                (url, title)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error adding history: {str(e)}")
            return False

    def get_history(self, limit=100):
        """Get recent history entries"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM history ORDER BY visited_at DESC LIMIT ?",
                (limit,)
            )
            history = cursor.fetchall()
            conn.close()
            return history
        except Exception as e:
            print(f"Error getting history: {str(e)}")
            return []

    def save_setting(self, key, value):
        """Save a setting"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
                (key, json.dumps(value))
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error saving setting: {str(e)}")
            return False

    def get_setting(self, key, default=None):
        """Get a setting value"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
            result = cursor.fetchone()
            conn.close()
            return json.loads(result[0]) if result else default
        except Exception as e:
            print(f"Error getting setting: {str(e)}")
            return default

    def add_download(self, filename, url, path, status="pending"):
        """Add a new download entry"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO downloads (filename, url, path, status) VALUES (?, ?, ?, ?)",
                (filename, url, path, status)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error adding download: {str(e)}")
            return False

    def update_download_status(self, download_id, status):
        """Update download status"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE downloads SET status = ? WHERE id = ?",
                (status, download_id)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating download status: {str(e)}")
            return False

    def get_downloads(self):
        """Get all downloads"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM downloads ORDER BY created_at DESC")
            downloads = cursor.fetchall()
            conn.close()
            return downloads
        except Exception as e:
            print(f"Error getting downloads: {str(e)}")
            return [] 