"""Helper utilities"""
import logging
from urllib.parse import urlparse
import re


class Logger:
    """Simple logging wrapper"""
    
    def __init__(self, name: str = "CometBrowser"):
        self.logger = logging.getLogger(name)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def info(self, msg: str):
        self.logger.info(msg)
    
    def error(self, msg: str):
        self.logger.error(msg)
    
    def warning(self, msg: str):
        self.logger.warning(msg)
    
    def debug(self, msg: str):
        self.logger.debug(msg)


class UrlValidator:
    """URL validation and normalization"""
    
    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Check if URL is valid"""
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # or IP
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return url_pattern.match(url) is not None
    
    @staticmethod
    def normalize_url(url: str) -> str:
        """Normalize URL - add protocol if missing, like Chrome"""
        url = url.strip()
        
        if not url:
            return "about:blank"
        
        # Already has protocol
        if re.match(r'^https?://', url):
            return url
        
        # Check if it's localhost
        if url.startswith('localhost'):
            return f"http://{url}"
        
        # Check if it's an IP address
        if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url):
            return f"http://{url}"
        
        # Has spaces - it's a search query
        if ' ' in url:
            return f"https://www.google.com/search?q={url.replace(' ', '+')}"
        
        # Check if it looks like a domain (has dot)
        if '.' in url:
            # Could be a domain
            parts = url.split('/')
            domain = parts[0]
            
            # Check if domain part doesn't have invalid characters
            if re.match(r'^[a-zA-Z0-9][a-zA-Z0-9-]*([.][a-zA-Z0-9][a-zA-Z0-9-]*)*$', domain):
                return f"https://{url}"
        
        # Everything else - search
        return f"https://www.google.com/search?q={url.replace(' ', '+')}"
    
    @staticmethod
    def get_domain(url: str) -> str:
        """Extract domain from URL"""
        try:
            parsed = urlparse(url)
            return parsed.netloc or parsed.path
        except:
            return url
