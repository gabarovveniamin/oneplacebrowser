"""User profile management system"""
import os
import json
from typing import Optional, Dict, List
from datetime import datetime


class ProfileManager:
    """Manage local user profiles"""
    
    def __init__(self):
        self.profiles_dir = os.path.expanduser("~/.comet_browser/profiles")
        self.profiles_file = os.path.join(
            os.path.dirname(self.profiles_dir), "profiles.json"
        )
        self.current_profile = None
        os.makedirs(self.profiles_dir, exist_ok=True)
        self.load_profiles()
    
    def load_profiles(self):
        """Load all profiles from file"""
        try:
            if os.path.exists(self.profiles_file):
                with open(self.profiles_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.current_profile = data.get('current_profile')
        except Exception as e:
            print(f"Error loading profiles: {e}")
    
    def get_all_profiles(self) -> List[Dict]:
        """Get list of all profiles"""
        profiles = []
        try:
            for profile_file in os.listdir(self.profiles_dir):
                if profile_file.endswith('.json'):
                    profile_path = os.path.join(self.profiles_dir, profile_file)
                    with open(profile_path, 'r', encoding='utf-8') as f:
                        profile = json.load(f)
                        profiles.append(profile)
        except Exception as e:
            print(f"Error reading profiles: {e}")
        
        return sorted(profiles, key=lambda p: p.get('created_at', ''), reverse=True)
    
    def create_profile(self, name: str, color: str = None) -> bool:
        """Create new profile"""
        try:
            profile_id = name.lower().replace(' ', '_')
            profile_path = os.path.join(self.profiles_dir, f"{profile_id}.json")
            
            # Don't overwrite existing profiles
            if os.path.exists(profile_path):
                return False
            
            profile_data = {
                'id': profile_id,
                'name': name,
                'color': color or '#4CAF50',
                'created_at': datetime.now().isoformat(),
                'last_used': datetime.now().isoformat()
            }
            
            with open(profile_path, 'w', encoding='utf-8') as f:
                json.dump(profile_data, f, indent=2, ensure_ascii=False)
            
            # Set as current profile
            self.set_current_profile(profile_id)
            return True
            
        except Exception as e:
            print(f"Error creating profile: {e}")
            return False
    
    def set_current_profile(self, profile_id: str) -> bool:
        """Set the current active profile"""
        try:
            profile_path = os.path.join(self.profiles_dir, f"{profile_id}.json")
            
            if not os.path.exists(profile_path):
                return False
            
            # Update last_used
            with open(profile_path, 'r', encoding='utf-8') as f:
                profile = json.load(f)
            
            profile['last_used'] = datetime.now().isoformat()
            
            with open(profile_path, 'w', encoding='utf-8') as f:
                json.dump(profile, f, indent=2, ensure_ascii=False)
            
            # Save current profile to main file
            data = {}
            if os.path.exists(self.profiles_file):
                with open(self.profiles_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            
            data['current_profile'] = profile_id
            
            with open(self.profiles_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self.current_profile = profile_id
            return True
            
        except Exception as e:
            print(f"Error setting profile: {e}")
            return False
    
    def get_current_profile(self) -> Optional[Dict]:
        """Get current profile data"""
        if not self.current_profile:
            return None
        
        try:
            profile_path = os.path.join(self.profiles_dir, f"{self.current_profile}.json")
            
            if os.path.exists(profile_path):
                with open(profile_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error reading profile: {e}")
        
        return None
    
    def delete_profile(self, profile_id: str) -> bool:
        """Delete a profile"""
        try:
            profile_path = os.path.join(self.profiles_dir, f"{profile_id}.json")
            
            if os.path.exists(profile_path):
                os.remove(profile_path)
                
                # If it was current profile, reset it
                if self.current_profile == profile_id:
                    self.current_profile = None
                    # Update file
                    data = {}
                    if os.path.exists(self.profiles_file):
                        with open(self.profiles_file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                    
                    data['current_profile'] = None
                    with open(self.profiles_file, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                
                return True
            return False
            
        except Exception as e:
            print(f"Error deleting profile: {e}")
            return False
    
    def profile_exists(self, profile_id: str) -> bool:
        """Check if profile exists"""
        profile_path = os.path.join(self.profiles_dir, f"{profile_id}.json")
        return os.path.exists(profile_path)
