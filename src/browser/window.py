"""Main browser window"""
import os
from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, 
    QPushButton, QLabel, QStackedWidget, QMenu, QMenuBar, QMessageBox
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QPixmap

from src.ui.widgets import AddressBar, TabBar
from src.ui.styles import ThemeManager, StyleManager
from src.ui.history import HistoryDialog, BookmarksDialog
from src.browser.tabs import TabManager
from src.storage.database import DatabaseManager
from src.auth.auth_manager import AuthManager
from src.auth.google_oauth import LoginDialog
from src.utils.helpers import UrlValidator, Logger


class BrowserWindow(QMainWindow):
    """Main browser window - Chrome-style"""
    
    def __init__(self):
        super().__init__()
        self.logger = Logger()
        self.url_validator = UrlValidator()
        self.tab_manager = TabManager()
        self.db_manager = DatabaseManager()
        self.theme_manager = ThemeManager()
        self.auth_manager = AuthManager()
        self.current_user_email = None
        
        self.setWindowTitle("Comet Browser")
        self.setGeometry(100, 100, 1400, 900)
        
        # Connect theme changes
        self.theme_manager.theme_changed.connect(self.apply_theme)
        
        # Apply initial theme
        self.apply_theme(self.theme_manager.current_theme.name)
        
        self.init_ui()
        
        # Show login dialog after UI is ready
        self.show_login_dialog()
        
        self.logger.info("Browser window initialized")
    
    def init_ui(self):
        """Initialize UI components"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create tab bar
        self.tab_bar = TabBar(self.theme_manager)
        self.tab_bar.tab_clicked.connect(self.on_tab_clicked)
        self.tab_bar.new_tab_requested.connect(self.create_new_tab)
        self.tab_bar.close_tab_requested.connect(self.on_close_tab)
        layout.addWidget(self.tab_bar)
        
        # Create navigation bar
        nav_layout = self.create_navigation_bar()
        layout.addLayout(nav_layout)
        
        # Create stacked widget for tabs
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)
        
        central_widget.setLayout(layout)
        
        # Create first tab with start page
        startpage_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'startpage.html')
        startpage_url = f"file:///{os.path.abspath(startpage_path).replace(chr(92), '/')}"
        self.create_new_tab(startpage_url)
    
    def create_menu_bar(self):
        """Create menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        file_menu.addAction("New Tab", self.create_new_tab)
        file_menu.addAction("New Window", self.new_window)
        file_menu.addSeparator()
        file_menu.addAction("Exit", self.close)
        
        # Edit menu
        edit_menu = menubar.addMenu("Edit")
        edit_menu.addAction("Clear History", self.clear_history)
        edit_menu.addAction("Clear Cache", self.clear_cache)
        
        # View menu
        view_menu = menubar.addMenu("View")
        view_menu.addAction("History", self.show_history)
        view_menu.addAction("Bookmarks", self.show_bookmarks)
        
        # Theme menu
        theme_menu = menubar.addMenu("Theme")
        light_action = theme_menu.addAction("Light Mode")
        dark_action = theme_menu.addAction("Dark Mode")
        theme_menu.addSeparator()
        toggle_action = theme_menu.addAction("Toggle Theme")
        
        light_action.triggered.connect(lambda: self.theme_manager.set_theme("light"))
        dark_action.triggered.connect(lambda: self.theme_manager.set_theme("dark"))
        toggle_action.triggered.connect(self.theme_manager.toggle_theme)
    
    def apply_theme(self, theme_name: str):
        """Apply theme to the entire application"""
        theme = self.theme_manager.current_theme
        
        # Apply main stylesheet
        self.setStyleSheet(StyleManager.get_stylesheet(theme))
        
        # Update address bar style
        if hasattr(self, 'address_bar'):
            self.address_bar.setStyleSheet(StyleManager.get_address_bar_stylesheet(theme))
        
        # Update tab bar styles (we'll need to update this after)
        if hasattr(self, 'tab_bar'):
            # Update nav buttons
            nav_btn_style = f"""
                QPushButton {{
                    background-color: transparent;
                    border: none;
                    color: {theme.colors['nav_text']};
                    font-size: 14px;
                    font-weight: bold;
                    padding: 4px 8px;
                    border-radius: 4px;
                }}
                QPushButton:hover {{
                    background-color: {theme.colors['button_hover']};
                    color: {theme.colors['text_primary']};
                }}
                QPushButton:pressed {{
                    background-color: {theme.colors['button_pressed']};
                }}
                QPushButton:disabled {{
                    color: {theme.colors['nav_disabled']};
                }}
            """
            
            # Apply to existing nav buttons
            if hasattr(self, 'back_btn'):
                self.back_btn.setStyleSheet(nav_btn_style)
            if hasattr(self, 'forward_btn'):
                self.forward_btn.setStyleSheet(nav_btn_style)
    
    def create_navigation_bar(self) -> QHBoxLayout:
        """Create Chrome-style navigation bar"""
        nav_layout = QHBoxLayout()
        nav_layout.setContentsMargins(8, 6, 8, 6)
        nav_layout.setSpacing(4)
        
        # Get styling from theme manager
        theme = self.theme_manager.current_theme
        nav_btn_style = f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                color: {theme.colors['nav_text']};
                font-size: 14px;
                font-weight: bold;
                padding: 4px 8px;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: {theme.colors['button_hover']};
                color: {theme.colors['text_primary']};
            }}
            QPushButton:pressed {{
                background-color: {theme.colors['button_pressed']};
            }}
            QPushButton:disabled {{
                color: {theme.colors['nav_disabled']};
            }}
        """
        
        # Back button
        back_btn = QPushButton("‹")
        back_btn.setMaximumWidth(36)
        back_btn.setMinimumHeight(32)
        back_btn.setStyleSheet(nav_btn_style)
        back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        back_btn.clicked.connect(self.go_back)
        nav_layout.addWidget(back_btn)
        self.back_btn = back_btn
        
        # Forward button
        forward_btn = QPushButton("›")
        forward_btn.setMaximumWidth(36)
        forward_btn.setMinimumHeight(32)
        forward_btn.setStyleSheet(nav_btn_style)
        forward_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        forward_btn.clicked.connect(self.go_forward)
        nav_layout.addWidget(forward_btn)
        self.forward_btn = forward_btn
        
        # Refresh button
        refresh_btn = QPushButton("↻")
        refresh_btn.setMaximumWidth(36)
        refresh_btn.setMinimumHeight(32)
        refresh_btn.setStyleSheet(nav_btn_style)
        refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh_btn.clicked.connect(self.refresh)
        nav_layout.addWidget(refresh_btn)
        self.refresh_btn = refresh_btn
        
        # Home button
        home_btn = QPushButton("⌂")
        home_btn.setMaximumWidth(36)
        home_btn.setMinimumHeight(32)
        home_btn.setStyleSheet(nav_btn_style)
        home_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        home_btn.clicked.connect(self.go_home)
        nav_layout.addWidget(home_btn)
        self.home_btn = home_btn
        
        # Address bar
        self.address_bar = AddressBar(self.theme_manager)
        self.address_bar.url_entered.connect(self.navigate)
        nav_layout.addWidget(self.address_bar)
        
        # Bookmark button
        bookmark_btn = QPushButton("☆")
        bookmark_btn.setMaximumWidth(36)
        bookmark_btn.setMinimumHeight(32)
        bookmark_btn.setStyleSheet(nav_btn_style)
        bookmark_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        bookmark_btn.clicked.connect(self.add_bookmark)
        nav_layout.addWidget(bookmark_btn)
        self.bookmark_btn = bookmark_btn
        
        # User label
        self.user_label = QLabel("Guest")
        self.user_label.setMaximumWidth(100)
        nav_layout.addWidget(self.user_label)
        
        # Menu button
        menu_btn = QPushButton("⋮")
        menu_btn.setMaximumWidth(36)
        menu_btn.setMinimumHeight(32)
        menu_btn.setStyleSheet(nav_btn_style)
        menu_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        menu_btn.clicked.connect(self.show_menu)
        nav_layout.addWidget(menu_btn)
        self.menu_btn = menu_btn
        
        return nav_layout
    
    def create_new_tab(self, url: str = None, is_first: bool = False):
        """Create new tab"""
        # Use start page if no URL provided
        if url is None or url == "about:blank":
            startpage_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'startpage.html')
            url = f"file:///{os.path.abspath(startpage_path).replace(chr(92), '/')}"
        
        web_view = QWebEngineView()
        web_view.setUrl(QUrl(self.url_validator.normalize_url(url) if url.startswith('file://') is False else url))
        
        # Connect events
        web_view.urlChanged.connect(self.on_url_changed)
        web_view.titleChanged.connect(self.on_title_changed)
        current_index = self.tab_bar.get_tab_count()
        
        self.stacked_widget.addWidget(web_view)
        self.stacked_widget.setCurrentWidget(web_view)
        
        # Add tab to tab bar
        self.tab_bar.add_tab("Стартовая страница")
        self.tab_bar.set_active_tab(current_index)
        
        # Add to tab manager
        self.tab_manager.create_tab(self.url_validator.normalize_url(url))
        
        self.logger.info(f"New tab created: {url}")
    
    def navigate(self, url: str):
        """Navigate to URL"""
        normalized_url = self.url_validator.normalize_url(url)
        web_view = self.stacked_widget.currentWidget()
        
        if web_view:
            web_view.setUrl(QUrl(normalized_url))
            self.address_bar.setText(normalized_url)
            
            # Add to history
            self.db_manager.add_to_history(normalized_url, user_email=self.current_user_email)
            self.logger.info(f"Navigated to: {normalized_url}")
    
    def go_back(self):
        """Go back in history"""
        web_view = self.stacked_widget.currentWidget()
        if web_view:
            web_view.back()
    
    def go_forward(self):
        """Go forward in history"""
        web_view = self.stacked_widget.currentWidget()
        if web_view:
            web_view.forward()
    
    def go_home(self):
        """Go to home page"""
        self.navigate("https://www.google.com")
    
    def refresh(self):
        """Refresh current page"""
        web_view = self.stacked_widget.currentWidget()
        if web_view:
            web_view.reload()
    
    def on_url_changed(self, url: QUrl):
        """Update address bar when URL changes"""
        self.address_bar.blockSignals(True)
        self.address_bar.setText(url.toString())
        self.address_bar.blockSignals(False)
    
    def on_title_changed(self, title: str):
        """Update window title when page title changes"""
        self.setWindowTitle(f"{title} - Comet Browser" if title else "Comet Browser")
        
        # Update tab title
        current_index = self.stacked_widget.currentIndex()
        if current_index >= 0:
            self.tab_bar.set_tab_title(current_index, title or "New Tab")
    
    def on_tab_clicked(self, index: int):
        """Handle tab click"""
        if 0 <= index < self.stacked_widget.count():
            self.stacked_widget.setCurrentIndex(index)
            self.tab_bar.set_active_tab(index)
            
            # Update address bar with current URL
            web_view = self.stacked_widget.widget(index)
            if web_view:
                self.address_bar.setText(web_view.url().toString())
    
    def on_close_tab(self, index: int):
        """Handle tab close"""
        if self.stacked_widget.count() <= 1:
            return  # Don't close last tab
        
        if 0 <= index < self.stacked_widget.count():
            widget = self.stacked_widget.widget(index)
            self.stacked_widget.removeWidget(widget)
            widget.deleteLater()
            
            self.tab_bar.remove_tab(index)
            
            # Switch to another tab
            remaining = self.stacked_widget.count()
            if remaining > 0:
                new_index = min(index, remaining - 1)
                self.stacked_widget.setCurrentIndex(new_index)
                self.tab_bar.set_active_tab(new_index)
                
                web_view = self.stacked_widget.widget(new_index)
                if web_view:
                    self.address_bar.setText(web_view.url().toString())
            
            self.logger.info(f"Tab closed: index {index}")
    
    def add_bookmark(self):
        """Add current page to bookmarks"""
        web_view = self.stacked_widget.currentWidget()
        if web_view:
            url = web_view.url().toString()
            title = web_view.title()
            if self.db_manager.add_bookmark(url, title, user_email=self.current_user_email):
                QMessageBox.information(self, "Success", "Bookmark added")
            else:
                QMessageBox.warning(self, "Info", "Bookmark already exists")
            self.logger.info(f"Bookmark added: {url}")
    
    def clear_history(self):
        """Clear browsing history"""
        reply = QMessageBox.question(
            self, 
            "Confirm",
            "Are you sure you want to clear all history?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.db_manager.clear_history(user_email=self.current_user_email)
            QMessageBox.information(self, "Success", "History cleared")
            self.logger.info("History cleared")
    
    def clear_cache(self):
        """Clear cache"""
        self.logger.info("Cache cleared")
    
    def show_history(self):
        """Show history dialog"""
        history_dialog = HistoryDialog(self.db_manager, user_email=self.current_user_email, parent=self)
        history_dialog.navigate_requested.connect(self.navigate)
        history_dialog.exec()
    
    def show_bookmarks(self):
        """Show bookmarks dialog"""
        bookmarks_dialog = BookmarksDialog(self.db_manager, user_email=self.current_user_email, parent=self)
        bookmarks_dialog.navigate_requested.connect(self.navigate)
        bookmarks_dialog.exec()
    
    def new_window(self):
        """Create new window"""
        self.logger.info("New window created")
    
    def show_menu(self):
        """Show browser menu"""
        self.logger.info("Menu opened")
    
    def show_login_dialog(self):
        """Show Google login dialog"""
        # Check if user already authenticated
        if self.auth_manager.is_authenticated:
            self.update_user_label()
            self.current_user_email = self.auth_manager.get_user_email()
            return
        
        login_dialog = LoginDialog(parent=self)
        login_dialog.login_successful.connect(self.on_login_successful)
        login_dialog.exec()
    
    def on_login_successful(self, profile_id: str):
        """Handle successful profile selection"""
        if self.auth_manager.save_user_data(profile_id):
            profile = self.auth_manager.get_current_user()
            if profile:
                # Update user label
                user_name = profile.get('name', 'User')
                self.user_label.setText(f"👤 {user_name}")
                
                # Update current user email (use profile id)
                self.current_user_email = profile_id
                
                self.logger.info(f"Profile activated: {user_name}")
        else:
            QMessageBox.warning(self, "Error", "Failed to activate profile")
    
    def update_user_label(self):
        """Update user label with current user info"""
        user_name = self.auth_manager.get_user_name()
        self.user_label.setText(f"👤 {user_name}")
    
    def closeEvent(self, event):
        """Handle window close"""
        self.db_manager.close()
        event.accept()
