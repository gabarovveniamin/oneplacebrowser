"""Authentication manager for the browser"""
import os
import json
from typing import Optional, Dict
from datetime import datetime
from src.auth.profile_manager import ProfileManager


class AuthManager:
    """Manage authentication and user sessions"""
    
    def __init__(self):
        self.profile_manager = ProfileManager()
        self.current_user = None
        self.is_authenticated = False
        self.load_user_data()
    
    def load_user_data(self):
        """Load current profile data"""
        try:
            profile = self.profile_manager.get_current_profile()
            if profile:
                self.current_user = profile
                self.is_authenticated = True
        except Exception as e:
            print(f"Error loading user data: {e}")
    
    def save_user_data(self, profile_id: str) -> bool:
        """Activate a profile"""
        try:
            if self.profile_manager.set_current_profile(profile_id):
                profile = self.profile_manager.get_current_profile()
                if profile:
                    self.current_user = profile
                    self.is_authenticated = True
                    return True
        except Exception as e:
            print(f"Error saving user data: {e}")
        
        return False
    
    def create_new_profile(self, name: str, color: str = None) -> bool:
        """Create new profile and activate it"""
        try:
            if self.profile_manager.create_profile(name, color):
                profile = self.profile_manager.get_current_profile()
                if profile:
                    self.current_user = profile
                    self.is_authenticated = True
                    return True
        except Exception as e:
            print(f"Error creating profile: {e}")
        
        return False
    
    def logout(self):
        """Logout current user"""
        self.current_user = None
        self.is_authenticated = False
    
    def get_current_user(self) -> Optional[Dict]:
        """Get current logged in user"""
        return self.current_user
    
    def get_user_name(self) -> str:
        """Get display name of current user"""
        if self.current_user:
            return self.current_user.get('name', 'User')
        return 'Guest'
    
    def get_user_email(self) -> Optional[str]:
        """Get email of current user - for profile, return profile ID"""
        if self.current_user:
            return self.current_user.get('id', 'guest')
        return None
    
    def get_all_profiles(self):
        """Get all available profiles"""
        return self.profile_manager.get_all_profiles()
