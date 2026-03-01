"""HTTP client for network requests"""
import requests
from typing import Optional, Dict


class HttpClient:
    """Handle HTTP requests with modern headers"""
    
    DEFAULT_HEADERS = {
        'User-Agent': 'CometBrowser/0.1.0 (Compatible with Chrome/120.0.0.0)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
    }
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(self.DEFAULT_HEADERS)
    
    def get(self, url: str, headers: Optional[Dict] = None) -> Optional[str]:
        """Fetch URL and return content"""
        try:
            if headers:
                self.session.headers.update(headers)
            
            response = self.session.get(url, timeout=self.timeout, allow_redirects=True)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def get_with_headers(self, url: str, headers: Dict = None) -> tuple:
        """Fetch URL and return content with headers"""
        try:
            if headers:
                self.session.headers.update(headers)
            
            response = self.session.get(url, timeout=self.timeout, allow_redirects=True)
            response.raise_for_status()
            return response.text, response.headers
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None, None
    
    def close(self):
        """Close session"""
        if self.session:
            self.session.close()


class CacheManager:
    """Simple in-memory cache for pages"""
    
    def __init__(self, max_size: int = 50):
        self.cache = {}
        self.max_size = max_size
    
    def get(self, url: str) -> Optional[str]:
        """Get cached content"""
        return self.cache.get(url)
    
    def set(self, url: str, content: str):
        """Cache content"""
        if len(self.cache) >= self.max_size:
            # Remove oldest item (simple FIFO)
            self.cache.pop(next(iter(self.cache)))
        self.cache[url] = content
    
    def clear(self):
        """Clear cache"""
        self.cache.clear()
