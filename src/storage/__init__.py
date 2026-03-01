"""Storage module - database, cookies, history"""

from .database import DatabaseManager
from .cookies import CookieStore

__all__ = ['DatabaseManager', 'CookieStore']
