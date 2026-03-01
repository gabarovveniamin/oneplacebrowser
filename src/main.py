"""Main entry point for CometBrowser"""
import sys
from PyQt6.QtWidgets import QApplication

from src.browser.window import BrowserWindow


def main():
    """Start the browser application"""
    app = QApplication(sys.argv)
    
    # Set application info
    app.setApplicationName("Comet Browser")
    app.setApplicationVersion("0.1.0")
    
    # Create and show main window
    window = BrowserWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
