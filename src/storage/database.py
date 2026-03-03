"""Database management for history, bookmarks, etc."""
import sqlite3
import os
from datetime import datetime
from typing import List, Tuple, Optional, Dict


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
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                email TEXT UNIQUE,
                name TEXT,
                photo_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # History table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY,
                url TEXT NOT NULL,
                title TEXT,
                visited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                user_email TEXT,
                FOREIGN KEY(user_email) REFERENCES users(email)
            )
        """)
        
        # Bookmarks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookmarks (
                id INTEGER PRIMARY KEY,
                url TEXT NOT NULL,
                title TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                user_email TEXT,
                UNIQUE(url, user_email),
                FOREIGN KEY(user_email) REFERENCES users(email)
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
    
    # User management methods
    def add_user(self, email: str, name: str, photo_url: str = None) -> bool:
        """Add or update user"""
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO users (email, name, photo_url, last_login)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            """, (email, name, photo_url))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error adding user: {e}")
            return False
    
    def get_user(self, email: str) -> Optional[Dict]:
        """Get user by email"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT email, name, photo_url, created_at FROM users WHERE email = ?", (email,))
        result = cursor.fetchone()
        if result:
            return {
                'email': result[0],
                'name': result[1],
                'photo_url': result[2],
                'created_at': result[3]
            }
        return None
    
    def update_last_login(self, email: str):
        """Update user's last login time"""
        cursor = self.conn.cursor()
        cursor.execute("UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE email = ?", (email,))
        self.conn.commit()
    
    # History methods
    def add_to_history(self, url: str, title: str = "", user_email: str = None):
        """Add URL to history"""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO history (url, title, user_email) VALUES (?, ?, ?)",
            (url, title, user_email)
        )
        self.conn.commit()
    
    def get_history(self, limit: int = 50, user_email: str = None) -> List[Tuple]:
        """Get recent history"""
        cursor = self.conn.cursor()
        if user_email:
            cursor.execute(
                "SELECT url, title, visited_at FROM history WHERE user_email = ? ORDER BY visited_at DESC LIMIT ?",
                (user_email, limit)
            )
        else:
            cursor.execute(
                "SELECT url, title, visited_at FROM history ORDER BY visited_at DESC LIMIT ?",
                (limit,)
            )
        return cursor.fetchall()
    
    def search_history(self, query: str, user_email: str = None) -> List[Tuple]:
        """Search history by URL or title"""
        cursor = self.conn.cursor()
        search_param = f"%{query}%"
        if user_email:
            cursor.execute(
                "SELECT url, title, visited_at FROM history WHERE (url LIKE ? OR title LIKE ?) AND user_email = ? ORDER BY visited_at DESC",
                (search_param, search_param, user_email)
            )
        else:
            cursor.execute(
                "SELECT url, title, visited_at FROM history WHERE url LIKE ? OR title LIKE ? ORDER BY visited_at DESC",
                (search_param, search_param)
            )
        return cursor.fetchall()
    
    def clear_history(self, user_email: str = None):
        """Clear history"""
        cursor = self.conn.cursor()
        if user_email:
            cursor.execute("DELETE FROM history WHERE user_email = ?", (user_email,))
        else:
            cursor.execute("DELETE FROM history")
        self.conn.commit()
    
    # Bookmark methods
    def add_bookmark(self, url: str, title: str = "", user_email: str = None):
        """Add URL to bookmarks"""
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO bookmarks (url, title, user_email) VALUES (?, ?, ?)",
                (url, title, user_email)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def get_bookmarks(self, user_email: str = None) -> List[Tuple]:
        """Get all bookmarks"""
        cursor = self.conn.cursor()
        if user_email:
            cursor.execute("SELECT url, title FROM bookmarks WHERE user_email = ? ORDER BY created_at DESC",
                         (user_email,))
        else:
            cursor.execute("SELECT url, title FROM bookmarks ORDER BY created_at DESC")
        return cursor.fetchall()
    
    def delete_bookmark(self, url: str, user_email: str = None):
        """Delete bookmark"""
        cursor = self.conn.cursor()
        if user_email:
            cursor.execute("DELETE FROM bookmarks WHERE url = ? AND user_email = ?", (url, user_email))
        else:
            cursor.execute("DELETE FROM bookmarks WHERE url = ?", (url,))
        self.conn.commit()
    
    def is_bookmarked(self, url: str, user_email: str = None) -> bool:
        """Check if URL is bookmarked"""
        cursor = self.conn.cursor()
        if user_email:
            cursor.execute("SELECT 1 FROM bookmarks WHERE url = ? AND user_email = ?", (url, user_email))
        else:
            cursor.execute("SELECT 1 FROM bookmarks WHERE url = ?", (url,))
        return cursor.fetchone() is not None
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

