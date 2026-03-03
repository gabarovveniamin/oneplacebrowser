"""UI Widgets - Address bar, tab bar, etc."""
from PyQt6.QtWidgets import (
    QLineEdit, QWidget, QHBoxLayout, QPushButton, QLabel,
    QScrollArea, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QFont, QIcon

from src.ui.styles import StyleManager


class AddressBar(QLineEdit):
    """Chrome-style address bar"""
    
    url_entered = pyqtSignal(str)
    
    def __init__(self, theme_manager=None):
        super().__init__()
        self.theme_manager = theme_manager
        self.setPlaceholderText("Search or enter address")
        self.setMinimumHeight(36)
        
        # Apply initial theme
        if self.theme_manager:
            self.update_theme()
            self.theme_manager.theme_changed.connect(self.on_theme_changed)
        else:
            # Fallback light theme
            self.setStyleSheet(StyleManager.get_address_bar_stylesheet(
                self.theme_manager.LIGHT_THEME if self.theme_manager else None
            ))
    
    def on_theme_changed(self, theme_name: str):
        """Update style when theme changes"""
        self.update_theme()
    
    def update_theme(self):
        """Update address bar theme"""
        theme = self.theme_manager.current_theme
        self.setStyleSheet(StyleManager.get_address_bar_stylesheet(theme))
    
    def keyPressEvent(self, event):
        """Handle Enter key"""
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.url_entered.emit(self.text())
        else:
            super().keyPressEvent(event)


class TabBar(QWidget):
    """Chrome-style tab bar for browser tabs"""
    
    tab_clicked = pyqtSignal(int)
    new_tab_requested = pyqtSignal()
    close_tab_requested = pyqtSignal(int)
    
    def __init__(self, theme_manager=None):
        super().__init__()
        self.tabs = []
        self.tab_buttons = []
        self.close_buttons = []
        self.current_index = -1
        self.theme_manager = theme_manager
        
        # Main layout для всей TAB BAR
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Layout для табов с LEFT alignment
        tabs_wrapper_layout = QHBoxLayout()
        tabs_wrapper_layout.setContentsMargins(0, 0, 0, 0)
        tabs_wrapper_layout.setSpacing(0)
        tabs_wrapper_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        
        # Scroll area for tabs
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll = scroll
        
        # Container for tabs внутри scroll
        self.tabs_container = QWidget()
        self.tabs_layout = QHBoxLayout()
        self.tabs_layout.setContentsMargins(0, 0, 0, 0)
        self.tabs_layout.setSpacing(-1)  # negative spacing для overlap
        self.tabs_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.tabs_container.setLayout(self.tabs_layout)
        
        # Add "+" button for new tab
        self.new_tab_btn = QPushButton("+")
        self.new_tab_btn.setMaximumWidth(40)
        self.new_tab_btn.setMinimumHeight(38)
        self.new_tab_btn.clicked.connect(self.new_tab_requested.emit)
        self.new_tab_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Добавляем + в конец layout табов
        self.tabs_layout.addWidget(self.new_tab_btn)
        # Добавляем stretch чтобы табы прижались влево
        self.tabs_layout.addStretch()
        
        scroll.setWidget(self.tabs_container)
        main_layout.addWidget(scroll)
        
        self.setLayout(main_layout)
        self.setMaximumHeight(38)
        
        # Apply theme
        if self.theme_manager:
            self.update_theme()
            self.theme_manager.theme_changed.connect(self.on_theme_changed)
        else:
            self.apply_light_theme()
    
    def on_theme_changed(self, theme_name: str):
        """Update style when theme changes"""
        self.update_theme()
    
    def update_theme(self):
        """Update tab bar styles with current theme"""
        theme = self.theme_manager.current_theme
        c = theme.colors
        
        # Scroll area
        scroll_style = f"""
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
        self.scroll.setStyleSheet(scroll_style)
        
        # Tabs container
        tabs_container_style = f"background-color: {c['bg_secondary']}; margin: 0px; padding: 0px;"
        self.tabs_container.setStyleSheet(tabs_container_style)
        
        # New tab button
        new_tab_style = f"""
            QPushButton {{
                background-color: {c['bg_secondary']};
                border: none;
                font-size: 18px;
                font-weight: bold;
                color: {c['nav_text']};
                padding: 0px 4px;
                margin: 0px;
                border-radius: 0px;
            }}
            QPushButton:hover {{
                background-color: {c['button_hover']};
                color: {c['text_primary']};
            }}
            QPushButton:pressed {{
                background-color: {c['button_pressed']};
            }}
        """
        self.new_tab_btn.setStyleSheet(new_tab_style)
        
        # Main widget
        main_style = f"""
            QWidget {{
                background-color: {c['bg_secondary']};
                border-bottom: 1px solid {c['border']};
                margin: 0px;
                padding: 0px;
            }}
        """
        self.setStyleSheet(main_style)
    
    def apply_light_theme(self):
        """Apply light theme as fallback"""
        light_scroll_style = """
            QScrollArea {
                background-color: #f3f3f3;
                border: none;
            }
            QScrollBar:horizontal {
                height: 6px;
            }
            QScrollBar::handle:horizontal {
                background: #bbb;
                border-radius: 3px;
            }
            QScrollBar::handle:horizontal:hover {
                background: #999;
            }
        """
        self.scroll.setStyleSheet(light_scroll_style)
        self.tabs_container.setStyleSheet("background-color: #f3f3f3; margin: 0px; padding: 0px;")
        
        light_new_tab_style = """
            QPushButton {
                background-color: #f3f3f3;
                border: none;
                font-size: 18px;
                font-weight: bold;
                color: #555;
                padding: 0px 4px;
                margin: 0px;
                border-radius: 0px;
            }
            QPushButton:hover {
                background-color: #e8e8e8;
                color: #222;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """
        self.new_tab_btn.setStyleSheet(light_new_tab_style)
        
        self.setStyleSheet("""
            QWidget {
                background-color: #f3f3f3;
                border-bottom: 1px solid #e0e0e0;
                margin: 0px;
                padding: 0px;
            }
        """)
    
    def add_tab(self, tab_name: str, index: int = None) -> QPushButton:
        """Add new tab with close button (Chrome-style compact)"""
        # Create tab widget with button and close X
        tab_container = QWidget()
        tab_layout = QHBoxLayout()
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.setSpacing(0)
        tab_container.setContentsMargins(0, 0, 0, 0)
        
        # Tab button
        tab_btn = QPushButton(tab_name)
        tab_index = len(self.tabs)
        tab_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        tab_btn.clicked.connect(lambda: self.tab_clicked.emit(tab_index))
        tab_btn.setMinimumWidth(50)
        tab_btn.setMaximumWidth(170)
        tab_btn.setMinimumHeight(38)
        tab_btn.setMaximumHeight(38)
        tab_btn.setStyleSheet(self._get_tab_stylesheet(False))
        
        tab_layout.addWidget(tab_btn)
        
        # Close button
        close_btn = QPushButton("✕")
        close_btn.setMaximumWidth(16)
        close_btn.setMaximumHeight(16)
        close_btn.setMinimumWidth(16)
        close_btn.setMinimumHeight(16)
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.clicked.connect(lambda: self.close_tab_requested.emit(tab_index))
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: #999;
                font-weight: bold;
                padding: 0px;
                font-size: 10px;
                margin: 0px 2px 0px 0px;
            }
            QPushButton:hover {
                color: #555;
                background-color: #d0d0d0;
                border-radius: 2px;
            }
        """)
        
        tab_layout.addWidget(close_btn)
        tab_container.setLayout(tab_layout)
        tab_container.setStyleSheet("""
            QWidget {
                background-color: #e8e8e8;
                margin: 0px;
                padding: 0px;
            }
        """)
        
        # Insert before the "+" button
        # Находим позицию кнопки "+"
        plus_pos = self.tabs_layout.indexOf(self.new_tab_btn)
        
        if index is not None:
            insert_pos = index
        else:
            insert_pos = len(self.tabs)
        
        # Вставляем таб перед "+" кнопкой
        self.tabs_layout.insertWidget(insert_pos, tab_container)
        self.tabs.insert(insert_pos, tab_container)
        self.tab_buttons.insert(insert_pos, tab_btn)
        self.close_buttons.insert(insert_pos, close_btn)
        
        return tab_btn
    
    def set_active_tab(self, index: int):
        """Set active tab"""
        if 0 <= index < len(self.tab_buttons):
            # Reset all tabs
            for i, btn in enumerate(self.tab_buttons):
                btn.setStyleSheet(self._get_tab_stylesheet(False))
            
            # Set active
            self.tab_buttons[index].setStyleSheet(self._get_tab_stylesheet(True))
            self.current_index = index
    
    def set_tab_title(self, index: int, title: str):
        """Update tab title"""
        if 0 <= index < len(self.tab_buttons):
            # Truncate long titles
            if len(title) > 25:
                title = title[:22] + "..."
            self.tab_buttons[index].setText(title)
    
    def remove_tab(self, index: int):
        """Remove tab by index"""
        if 0 <= index < len(self.tabs):
            self.tabs[index].deleteLater()
            self.tabs.pop(index)
            self.tab_buttons.pop(index)
            self.close_buttons.pop(index)
            
            if self.current_index >= len(self.tabs):
                self.current_index = len(self.tabs) - 1
    
    def get_tab_count(self) -> int:
        """Get number of tabs"""
        return len(self.tabs)
    
    @staticmethod
    def _get_tab_stylesheet(is_active: bool) -> str:
        """Get Chrome-style stylesheet for tab button"""
        if is_active:
            return """
                QPushButton {
                    background-color: #ffffff;
                    border: 1px solid #dadada;
                    border-bottom: none;
                    padding: 4px 10px;
                    border-radius: 6px 6px 0px 0px;
                    font-weight: 500;
                    color: #222;
                    font-size: 12px;
                    margin: 0px;
                }
                QPushButton:pressed {
                    background-color: #ffffff;
                }
            """
        else:
            return """
                QPushButton {
                    background-color: #e8e8e8;
                    border: none;
                    padding: 4px 10px;
                    color: #666;
                    font-size: 12px;
                    border-radius: 0px;
                    margin: 0px;
                }
                QPushButton:hover {
                    background-color: #d9d9d9;
                    color: #333;
                }
                QPushButton:pressed {
                    background-color: #d0d0d0;
                }
            """
