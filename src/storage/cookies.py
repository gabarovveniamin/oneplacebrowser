"""Cookie management"""
import sqlite3
import os
from datetime import datetime


class CookieStore:
    """Manage cookies"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            app_data = os.path.expanduser("~/.comet_browser")
            os.makedirs(app_data, exist_ok=True)
            db_path = os.path.join(app_data, "cookies.db")
        
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.init_cookies_table()
    
    def init_cookies_table(self):
        """Initialize cookies table"""
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cookies (
                id INTEGER PRIMARY KEY,
                domain TEXT NOT NULL,
                name TEXT NOT NULL,
                value TEXT,
                path TEXT DEFAULT '/',
                expires_at TIMESTAMP,
                secure BOOLEAN DEFAULT 0,
                http_only BOOLEAN DEFAULT 0,
                UNIQUE(domain, name, path)
            )
        """)
        self.conn.commit()
    
    def set_cookie(self, domain: str, name: str, value: str, 
                   path: str = "/", expires: str = None, 
                   secure: bool = False, http_only: bool = False):
        """Set a cookie"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO cookies 
            (domain, name, value, path, expires_at, secure, http_only)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (domain, name, value, path, expires, secure, http_only))
        self.conn.commit()
    
    def get_cookies(self, domain: str) -> list:
        """Get cookies for domain"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT name, value FROM cookies 
            WHERE domain = ? AND (expires_at IS NULL OR expires_at > datetime('now'))
        """, (domain,))
        return cursor.fetchall()
    
    def clear_cookies(self):
        """Clear all cookies"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM cookies")
        self.conn.commit()
    
    def close(self):
        """Close connection"""
        if self.conn:
            self.conn.close()
