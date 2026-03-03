"""History and bookmarks UI components"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, 
    QLineEdit, QPushButton, QMessageBox, QLabel, QWidget, QHeaderView
)
from PyQt6.QtCore import Qt, pyqtSignal, QUrl
from PyQt6.QtGui import QFont
from datetime import datetime


class HistoryDialog(QDialog):
    """Dialog for viewing and managing browsing history"""
    
    navigate_requested = pyqtSignal(str)  # Emits URL when user wants to navigate
    
    def __init__(self, db_manager, user_email: str = None, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.user_email = user_email
        self.init_ui()
        self.load_history()
        self.setWindowTitle("Browsing History")
        self.setGeometry(100, 100, 1000, 600)
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Browsing History")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Search bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search history...")
        self.search_input.textChanged.connect(self.on_search)
        search_layout.addWidget(self.search_input)
        
        clear_btn = QPushButton("Clear History")
        clear_btn.clicked.connect(self.on_clear_history)
        search_layout.addWidget(clear_btn)
        layout.addLayout(search_layout)
        
        # History table
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(3)
        self.history_table.setHorizontalHeaderLabels(["URL", "Title", "Visited"])
        self.history_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.history_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.history_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.history_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.history_table.doubleClicked.connect(self.on_item_activated)
        layout.addWidget(self.history_table)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        open_btn = QPushButton("Open")
        open_btn.clicked.connect(self.on_item_activated)
        button_layout.addWidget(open_btn)
        
        delete_btn = QPushButton("Delete")
        delete_btn.clicked.connect(self.on_delete_selected)
        button_layout.addWidget(delete_btn)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.reject)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def load_history(self):
        """Load history from database"""
        history = self.db_manager.get_history(limit=500, user_email=self.user_email)
        self.history_table.setRowCount(len(history))
        
        for row, (url, title, visited_at) in enumerate(history):
            # URL
            url_item = QTableWidgetItem(url)
            url_item.setData(Qt.ItemDataRole.UserRole, url)  # Store full URL
            self.history_table.setItem(row, 0, url_item)
            
            # Title
            title_text = title if title else "No title"
            self.history_table.setItem(row, 1, QTableWidgetItem(title_text))
            
            # Visited time
            try:
                dt = datetime.fromisoformat(visited_at)
                time_str = dt.strftime("%H:%M:%S")
                date_str = dt.strftime("%Y-%m-%d")
                self.history_table.setItem(row, 2, QTableWidgetItem(f"{date_str} {time_str}"))
            except:
                self.history_table.setItem(row, 2, QTableWidgetItem(visited_at))
    
    def on_search(self, query: str):
        """Handle history search"""
        if not query:
            self.load_history()
            return
        
        results = self.db_manager.search_history(query, user_email=self.user_email)
        self.history_table.setRowCount(len(results))
        
        for row, (url, title, visited_at) in enumerate(results):
            self.history_table.setItem(row, 0, QTableWidgetItem(url))
            self.history_table.setItem(row, 1, QTableWidgetItem(title or "No title"))
            try:
                dt = datetime.fromisoformat(visited_at)
                time_str = dt.strftime("%H:%M:%S")
                date_str = dt.strftime("%Y-%m-%d")
                self.history_table.setItem(row, 2, QTableWidgetItem(f"{date_str} {time_str}"))
            except:
                self.history_table.setItem(row, 2, QTableWidgetItem(visited_at))
    
    def on_item_activated(self):
        """Handle item double-click or open button"""
        current_row = self.history_table.currentRow()
        if current_row >= 0:
            url = self.history_table.item(current_row, 0).text()
            self.navigate_requested.emit(url)
            self.accept()
    
    def on_delete_selected(self):
        """Delete selected history item"""
        current_row = self.history_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select an item to delete")
            return
        
        url = self.history_table.item(current_row, 0).text()
        # Note: We can delete individual entries but SQLite doesn't have DELETE WHERE url AND time
        # For now, we'll just reload history
        QMessageBox.information(self, "Info", "Delete functionality coming soon")
    
    def on_clear_history(self):
        """Clear all history"""
        reply = QMessageBox.question(
            self, 
            "Confirm",
            "Are you sure you want to clear all history?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.db_manager.clear_history(user_email=self.user_email)
            self.history_table.setRowCount(0)
            QMessageBox.information(self, "Success", "History cleared")


class BookmarksDialog(QDialog):
    """Dialog for viewing and managing bookmarks"""
    
    navigate_requested = pyqtSignal(str)
    
    def __init__(self, db_manager, user_email: str = None, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.user_email = user_email
        self.init_ui()
        self.load_bookmarks()
        self.setWindowTitle("Bookmarks")
        self.setGeometry(100, 100, 1000, 600)
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Bookmarks")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Bookmarks table
        self.bookmarks_table = QTableWidget()
        self.bookmarks_table.setColumnCount(2)
        self.bookmarks_table.setHorizontalHeaderLabels(["URL", "Title"])
        self.bookmarks_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.bookmarks_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.bookmarks_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.bookmarks_table.doubleClicked.connect(self.on_item_activated)
        layout.addWidget(self.bookmarks_table)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        open_btn = QPushButton("Open")
        open_btn.clicked.connect(self.on_item_activated)
        button_layout.addWidget(open_btn)
        
        delete_btn = QPushButton("Delete Bookmark")
        delete_btn.clicked.connect(self.on_delete_bookmark)
        button_layout.addWidget(delete_btn)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.reject)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def load_bookmarks(self):
        """Load bookmarks from database"""
        bookmarks = self.db_manager.get_bookmarks(user_email=self.user_email)
        self.bookmarks_table.setRowCount(len(bookmarks))
        
        for row, (url, title) in enumerate(bookmarks):
            self.bookmarks_table.setItem(row, 0, QTableWidgetItem(url))
            self.bookmarks_table.setItem(row, 1, QTableWidgetItem(title or ""))
    
    def on_item_activated(self):
        """Handle item double-click"""
        current_row = self.bookmarks_table.currentRow()
        if current_row >= 0:
            url = self.bookmarks_table.item(current_row, 0).text()
            self.navigate_requested.emit(url)
            self.accept()
    
    def on_delete_bookmark(self):
        """Delete selected bookmark"""
        current_row = self.bookmarks_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a bookmark to delete")
            return
        
        url = self.bookmarks_table.item(current_row, 0).text()
        self.db_manager.delete_bookmark(url, user_email=self.user_email)
        self.bookmarks_table.removeRow(current_row)
        QMessageBox.information(self, "Success", "Bookmark deleted")
