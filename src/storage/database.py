"""Database management for history, bookmarks, etc."""
import sqlite3
import os
from datetime import datetime
from typing import List, Tuple


class DatabaseManager:
    """Manage SQLite database for browser data"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            app_data = os.path.expanduser("~/.comet_browser")
            os.makedirs(app_data, exist_ok=True)
            db_path = os.path.join(app_data, "browser.db")
        
        self.db_path = db_path
        self.conn = None
        self.init_db()
    
    def init_db(self):
        """Initialize database with tables"""
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()
        
        # History table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY,
                url TEXT NOT NULL,
                title TEXT,
                visited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Bookmarks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookmarks (
                id INTEGER PRIMARY KEY,
                url TEXT NOT NULL UNIQUE,
                title TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Cookies table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cookies (
                id INTEGER PRIMARY KEY,
                domain TEXT NOT NULL,
                name TEXT NOT NULL,
                value TEXT,
                expires_at TIMESTAMP,
                UNIQUE(domain, name)
            )
        """)
        
        self.conn.commit()
    
    def add_to_history(self, url: str, title: str = ""):
        """Add URL to history"""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO history (url, title) VALUES (?, ?)",
            (url, title)
        )
        self.conn.commit()
    
    def get_history(self, limit: int = 50) -> List[Tuple]:
        """Get recent history"""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT url, title, visited_at FROM history ORDER BY visited_at DESC LIMIT ?",
            (limit,)
        )
        return cursor.fetchall()
    
    def add_bookmark(self, url: str, title: str = ""):
        """Add URL to bookmarks"""
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO bookmarks (url, title) VALUES (?, ?)",
                (url, title)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def get_bookmarks(self) -> List[Tuple]:
        """Get all bookmarks"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT url, title FROM bookmarks ORDER BY created_at DESC")
        return cursor.fetchall()
    
    def delete_bookmark(self, url: str):
        """Delete bookmark"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM bookmarks WHERE url = ?", (url,))
        self.conn.commit()
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
