"""Tab management for browser"""
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl


class TabManager:
    """Manage browser tabs"""
    
    def __init__(self):
        self.tabs = []
        self.current_tab = None
    
    def create_tab(self, url: str = "about:blank") -> QWebEngineView:
        """Create new tab with WebEngine"""
        web_view = QWebEngineView()
        web_view.setUrl(QUrl(url))
        self.tabs.append(web_view)
        self.current_tab = web_view
        return web_view
    
    def close_tab(self, index: int) -> bool:
        """Close tab by index"""
        if 0 <= index < len(self.tabs):
            self.tabs[index].deleteLater()
            self.tabs.pop(index)
            if self.tabs:
                self.current_tab = self.tabs[0]
            else:
                self.current_tab = None
            return True
        return False
    
    def get_tab(self, index: int) -> QWebEngineView:
        """Get tab by index"""
        if 0 <= index < len(self.tabs):
            return self.tabs[index]
        return None
    
    def get_current_tab(self) -> QWebEngineView:
        """Get current active tab"""
        return self.current_tab
    
    def set_current_tab(self, index: int):
        """Set current active tab"""
        if 0 <= index < len(self.tabs):
            self.current_tab = self.tabs[index]
            return True
        return False
    
    def get_tab_count(self) -> int:
        """Get total number of tabs"""
        return len(self.tabs)
