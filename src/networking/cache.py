"""Network cache for pages"""

class CacheManager:
    """Simple in-memory cache for pages"""
    
    def __init__(self, max_size: int = 50):
        self.cache = {}
        self.max_size = max_size
    
    def get(self, url: str):
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
    
    def has(self, url: str) -> bool:
        """Check if URL is cached"""
        return url in self.cache
