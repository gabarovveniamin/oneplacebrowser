"""Styles module"""

class StyleManager:
    """Manage application styles"""
    
    @staticmethod
    def get_dark_stylesheet() -> str:
        """Get dark theme stylesheet"""
        return """
            QMainWindow {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QMenuBar {
                background-color: #2d2d2d;
                color: #ffffff;
            }
            QLineEdit {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #3d3d3d;
            }
        """
    
    @staticmethod
    def get_light_stylesheet() -> str:
        """Get light theme stylesheet"""
        return ""
