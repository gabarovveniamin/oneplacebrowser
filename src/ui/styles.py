"""Styles module"""
from PyQt6.QtCore import QObject, pyqtSignal


class Theme:
    """Theme colors and styles"""
    
    def __init__(self, name: str, colors: dict):
        self.name = name
        self.colors = colors


class ThemeManager(QObject):
    """Manage application themes with signals"""
    
    theme_changed = pyqtSignal(str)  # Emits theme name
    
    LIGHT_THEME = Theme("light", {
        "bg_main": "#ffffff",
        "bg_secondary": "#f3f3f3",
        "bg_tertiary": "#ebebeb",
        "text_primary": "#202124",
        "text_secondary": "#555555",
        "border": "#dadada",
        "highlight": "#4285f4",
        "hover": "#ebebeb",
        "menu_bg": "#ffffff",
        "button_hover": "#e8e8e8",
        "button_pressed": "#d0d0d0",
        "nav_text": "#555",
        "nav_disabled": "#ccc",
        "scroll_handle": "#bbb",
        "scroll_handle_hover": "#999",
    })
    
    DARK_THEME = Theme("dark", {
        "bg_main": "#1e1e1e",
        "bg_secondary": "#2d2d2d",
        "bg_tertiary": "#3d3d3d",
        "text_primary": "#e0e0e0",
        "text_secondary": "#b0b0b0",
        "border": "#454545",
        "highlight": "#5c9cff",
        "hover": "#3a3a3a",
        "menu_bg": "#2d2d2d",
        "button_hover": "#3a3a3a",
        "button_pressed": "#454545",
        "nav_text": "#b0b0b0",
        "nav_disabled": "#656565",
        "scroll_handle": "#555555",
        "scroll_handle_hover": "#777777",
    })
    
    def __init__(self):
        super().__init__()
        self.current_theme = self.LIGHT_THEME
    
    def set_theme(self, theme_name: str):
        """Set the current theme"""
        if theme_name == "dark":
            self.current_theme = self.DARK_THEME
        else:
            self.current_theme = self.LIGHT_THEME
        self.theme_changed.emit(theme_name)
    
    def get_current_theme(self) -> Theme:
        """Get current theme"""
        return self.current_theme
    
    def toggle_theme(self):
        """Toggle between light and dark theme"""
        if self.current_theme.name == "light":
            self.set_theme("dark")
        else:
            self.set_theme("light")


class StyleManager:
    """Manage application styles"""
    
    @staticmethod
    def get_stylesheet(theme: Theme) -> str:
        """Get stylesheet for given theme"""
        c = theme.colors
        return f"""
            QMainWindow {{
                background-color: {c['bg_main']};
                color: {c['text_primary']};
            }}
            
            QMenuBar {{
                background-color: {c['menu_bg']};
                color: {c['text_primary']};
                border-bottom: 1px solid {c['border']};
            }}
            
            QMenuBar::item:selected {{
                background-color: {c['bg_tertiary']};
            }}
            
            QMenu {{
                background-color: {c['bg_secondary']};
                color: {c['text_primary']};
                border: 1px solid {c['border']};
            }}
            
            QMenu::item:selected {{
                background-color: {c['highlight']};
                color: {c['bg_main']};
            }}
            
            QLineEdit {{
                padding: 8px 12px;
                border: 1px solid {c['border']};
                border-radius: 24px;
                font-size: 13px;
                background-color: {c['bg_secondary']};
                color: {c['text_primary']};
                selection-background-color: {c['highlight']};
            }}
            
            QLineEdit:focus {{
                border: 2px solid {c['highlight']};
                background-color: {c['bg_main']};
                padding: 7px 11px;
            }}
            
            QLineEdit:hover {{
                background-color: {c['hover']};
            }}
            
            QPushButton {{
                background-color: transparent;
                border: none;
                color: {c['nav_text']};
                font-size: 14px;
                font-weight: bold;
                padding: 4px 8px;
                border-radius: 4px;
            }}
            
            QPushButton:hover {{
                background-color: {c['button_hover']};
                color: {c['text_primary']};
            }}
            
            QPushButton:pressed {{
                background-color: {c['button_pressed']};
            }}
            
            QPushButton:disabled {{
                color: {c['nav_disabled']};
            }}
            
            QScrollArea {{
                background-color: {c['bg_secondary']};
                border: none;
            }}
            
            QScrollBar:horizontal {{
                height: 6px;
                background-color: {c['bg_secondary']};
            }}
            
            QScrollBar::handle:horizontal {{
                background: {c['scroll_handle']};
                border-radius: 3px;
            }}
            
            QScrollBar::handle:horizontal:hover {{
                background: {c['scroll_handle_hover']};
            }}
            
            QScrollBar:vertical {{
                width: 6px;
                background-color: {c['bg_secondary']};
            }}
            
            QScrollBar::handle:vertical {{
                background: {c['scroll_handle']};
                border-radius: 3px;
            }}
            
            QScrollBar::handle:vertical:hover {{
                background: {c['scroll_handle_hover']};
            }}
            
            QLabel {{
                color: {c['text_primary']};
            }}
        """
    
    @staticmethod
    def get_address_bar_stylesheet(theme: Theme) -> str:
        """Get address bar stylesheet"""
        c = theme.colors
        return f"""
            QLineEdit {{
                padding: 8px 12px;
                border: 1px solid {c['border']};
                border-radius: 24px;
                font-size: 13px;
                background-color: {c['bg_secondary']};
                color: {c['text_primary']};
                selection-background-color: {c['highlight']};
            }}
            QLineEdit:focus {{
                border: 2px solid {c['highlight']};
                background-color: {c['bg_main']};
                padding: 7px 11px;
            }}
            QLineEdit:hover {{
                background-color: {c['hover']};
            }}
        """
    
    @staticmethod
    def get_tab_bar_stylesheet(theme: Theme) -> str:
        """Get tab bar stylesheet"""
        c = theme.colors
        return f"""
            QScrollArea {{
                background-color: {c['bg_secondary']};
                border: none;
            }}
            QScrollBar:horizontal {{
                height: 6px;
            }}
            QScrollBar::handle:horizontal {{
                background: {c['scroll_handle']};
                border-radius: 3px;
            }}
            QScrollBar::handle:horizontal:hover {{
                background: {c['scroll_handle_hover']};
            }}
        """
    
    @staticmethod
    def get_nav_button_stylesheet(theme: Theme) -> str:
        """Get navigation button stylesheet"""
        c = theme.colors
        return f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                color: {c['nav_text']};
                font-size: 14px;
                font-weight: bold;
                padding: 4px 8px;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: {c['button_hover']};
                color: {c['text_primary']};
            }}
            QPushButton:pressed {{
                background-color: {c['button_pressed']};
            }}
            QPushButton:disabled {{
                color: {c['nav_disabled']};
            }}
        """
