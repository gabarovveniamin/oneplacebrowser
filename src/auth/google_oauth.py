"""Profile selection and creation UI"""
import json
import os
from typing import Optional, Dict
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QMessageBox, QInputDialog, QLineEdit, QScrollArea, QWidget, QGridLayout
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QIcon
from src.auth.profile_manager import ProfileManager


class LoginDialog(QDialog):
    """Profile selection and creation dialog"""
    
    login_successful = pyqtSignal(str)  # Emits profile_id
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.profile_manager = ProfileManager()
        self.setWindowTitle("Comet Browser - Select Profile")
        self.setGeometry(300, 200, 600, 500)
        self.setModal(True)
        
        # Styling
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
                color: #000000;
            }
            QLabel {
                color: #000000;
                background-color: #ffffff;
            }
            QPushButton {
                background-color: #f0f0f0;
                color: #000000;
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 10px;
                font-size: 13px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
                border: 1px solid #999999;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
            QScrollArea {
                background-color: #ffffff;
                border: none;
            }
        """)
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("👤 Select or Create Profile")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Description
        desc = QLabel("Choose an existing profile or create a new one")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_font = QFont()
        desc_font.setPointSize(10)
        desc.setFont(desc_font)
        layout.addWidget(desc)
        
        layout.addSpacing(10)
        
        # Profiles area
        profiles = self.profile_manager.get_all_profiles()
        
        if profiles:
            # Scroll area for profile buttons
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll_widget = QWidget()
            scroll_layout = QGridLayout(scroll_widget)
            scroll_layout.setSpacing(10)
            
            col = 0
            for i, profile in enumerate(profiles):
                btn = self.create_profile_button(profile)
                scroll_layout.addWidget(btn, i // 2, i % 2)
            
            scroll_layout.addStretch()
            scroll.setWidget(scroll_widget)
            layout.addWidget(QLabel("Your Profiles:"))
            layout.addWidget(scroll, 1)
        else:
            # No profiles yet
            no_profiles = QLabel("No profiles yet. Create one to get started!")
            no_profiles.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_profiles_font = QFont()
            no_profiles_font.setPointSize(11)
            no_profiles_font.setItalic(True)
            no_profiles.setFont(no_profiles_font)
            layout.addWidget(no_profiles)
            layout.addSpacing(20)
        
        # Create new profile button
        new_btn = QPushButton("➕ Create New Profile")
        new_btn.setMinimumHeight(50)
        new_btn.clicked.connect(self.on_create_profile)
        new_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: #ffffff;
                border: none;
                border-radius: 4px;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        layout.addWidget(new_btn)
        
        layout.addSpacing(5)
        
        # Cancel button
        cancel_btn = QPushButton("✕ Exit")
        cancel_btn.setMinimumHeight(40)
        cancel_btn.clicked.connect(self.reject)
        layout.addWidget(cancel_btn)
        
        self.setLayout(layout)
    
    def create_profile_button(self, profile: Dict) -> QPushButton:
        """Create a button for a profile"""
        btn = QPushButton()
        
        name = profile.get('name', 'Unknown')
        color = profile.get('color', '#4CAF50')
        profile_id = profile.get('id', '')
        
        # Button text
        last_used = profile.get('last_used', '').split('T')[0]
        btn.setText(f"{name}\n{last_used}")
        btn.setMinimumHeight(80)
        
        # Style button with profile color
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: #ffffff;
                border: 2px solid {color};
                border-radius: 6px;
                padding: 10px;
                font-size: 12px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                border: 2px solid #000000;
            }}
            QPushButton:pressed {{
                background-color: #333333;
                border: 2px solid #000000;
            }}
        """)
        
        btn.clicked.connect(lambda: self.select_profile(profile_id))
        return btn
    
    def select_profile(self, profile_id: str):
        """Select a profile"""
        self.login_successful.emit(profile_id)
        self.accept()
    
    def on_create_profile(self):
        """Handle create new profile"""
        name, ok = QInputDialog.getText(
            self,
            "New Profile",
            "Enter profile name:",
            QLineEdit.EchoMode.Normal,
            "My Profile"
        )
        
        if ok and name:
            # Color selection
            colors = [
                '#4CAF50',  # Green
                '#2196F3',  # Blue
                '#FF9800',  # Orange
                '#9C27B0',  # Purple
                '#F44336',  # Red
                '#00BCD4',  # Cyan
            ]
            
            color_names = [
                'Green',
                'Blue',
                'Orange',
                'Purple',
                'Red',
                'Cyan'
            ]
            
            color, ok2 = QInputDialog.getItem(
                self,
                "Choose Color",
                "Select profile color:",
                color_names,
                0,
                False
            )
            
            if ok2:
                color_hex = colors[color_names.index(color)]
                
                if self.profile_manager.create_profile(name, color_hex):
                    profile = self.profile_manager.get_current_profile()
                    if profile:
                        self.login_successful.emit(profile.get('id'))
                        self.accept()
                else:
                    QMessageBox.warning(
                        self,
                        "Error",
                        f"Profile '{name}' already exists!"
                    )
