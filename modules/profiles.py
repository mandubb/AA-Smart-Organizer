"""
Profiles Module
Manages user profiles with separate configurations and logs
"""

from pathlib import Path
from typing import List, Optional, Dict, Any
from .utils import (
    ensure_directory, load_json, save_json,
    get_timestamp
)


class ProfileManager:
    """Manages user profiles for the application"""
    
    DEFAULT_CONFIG = {
        "file_types": {
            "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".xls", ".pptx", ".ppt", ".odt", ".rtf", ".csv", ".md"],
            "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".ico", ".webp", ".tiff", ".heic", ".raw", ".jfif"],
            "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".m4v", ".3gp", ".mts"],
            "Music": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a", ".mid", ".midi"],
            "Installers": [".exe", ".msi", ".dmg", ".pkg", ".deb", ".rpm", ".apk", ".appimage"],
            "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".iso"],
            "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".h", ".json", ".xml", ".sql", ".php", ".ts", ".sh", ".bat", ".yml", ".yaml"],
            "Game Files": [".iso", ".bin", ".cue", ".sav", ".pak", ".vpk", ".wad", ".rom", ".nes", ".gba", ".n64", ".rpf"],
            "System": [".bat", ".cmd", ".reg", ".inf", ".sys", ".dll", ".ini", ".cfg", ".log", ".tmp"],
            "Design": [".psd", ".ai", ".xd", ".fig", ".blend", ".fbx", ".obj", ".3ds", ".prproj", ".aep", ".kra", ".xcf", ".dwg", ".dxf", ".skp", ".layout", ".style"],
            "Backups": [".img", ".vhd", ".vhdx", ".bak", ".gho", ".tar.gz"],
            "eBooks": [".epub", ".mobi", ".azw3", ".cbz", ".cbr", ".pdf"],
            "Plugins & Mods": [".dll", ".pak", ".vst", ".vst3", ".esp", ".bsa", ".mod", ".asi"],
            "Torrents": [".torrent"],
            "Miscellaneous": []
        },
        "enable_activity_log": True,
        "enable_quick_clean": True,
        "enable_summary": True,
        "enable_scheduler": False,
        "log_rotation_days": 30
    }
    
    def __init__(self, profiles_directory: Path):
        """
        Initialize profile manager
        
        Args:
            profiles_directory: Base directory for all profiles
        """
        self.profiles_directory = Path(profiles_directory)
        ensure_directory(self.profiles_directory)
        
        self.current_profile: Optional[str] = None
        self.current_profile_path: Optional[Path] = None
        
        # Ensure default profile exists
        self._ensure_default_profile()
    
    def _ensure_default_profile(self) -> None:
        """Ensure default profile exists"""
        default_path = self.profiles_directory / "default"
        if not default_path.exists():
            self.create_profile("default")
    
    def create_profile(self, profile_name: str) -> bool:
        """
        Create a new profile
        
        Args:
            profile_name: Name of the profile
            
        Returns:
            bool: True if successful
        """
        profile_path = self.profiles_directory / profile_name
        
        if profile_path.exists():
            print(f"⚠️ Profile '{profile_name}' already exists")
            return False
        
        try:
            # Create profile directory structure
            ensure_directory(profile_path)
            ensure_directory(profile_path / "logs")
            
            # Create default config
            config_path = profile_path / "config.json"
            save_json(config_path, self.DEFAULT_CONFIG)
            
            # Create profile metadata
            metadata = {
                "name": profile_name,
                "created": get_timestamp(),
                "last_used": get_timestamp(),
                "description": f"Profile for {profile_name}"
            }
            save_json(profile_path / "metadata.json", metadata)
            
            print(f"✅ Created profile: {profile_name}")
            return True
        
        except Exception as e:
            print(f"❌ Error creating profile: {e}")
            return False
    
    def list_profiles(self) -> List[str]:
        """
        List all available profiles
        
        Returns:
            List of profile names
        """
        profiles = []
        
        try:
            for item in self.profiles_directory.iterdir():
                if item.is_dir() and (item / "config.json").exists():
                    profiles.append(item.name)
        except Exception as e:
            print(f"❌ Error listing profiles: {e}")
        
        return sorted(profiles)
    
    def load_profile(self, profile_name: str) -> bool:
        """
        Load a profile
        
        Args:
            profile_name: Name of the profile to load
            
        Returns:
            bool: True if successful
        """
        profile_path = self.profiles_directory / profile_name
        
        if not profile_path.exists():
            print(f"❌ Profile '{profile_name}' not found")
            return False
        
        config_path = profile_path / "config.json"
        if not config_path.exists():
            print(f"❌ Profile '{profile_name}' has no config file")
            return False
        
        self.current_profile = profile_name
        self.current_profile_path = profile_path
        
        # Update last used timestamp
        metadata_path = profile_path / "metadata.json"
        metadata = load_json(metadata_path, {})
        metadata['last_used'] = get_timestamp()
        save_json(metadata_path, metadata)
        
        print(f"✅ Loaded profile: {profile_name}")
        return True
    
    def get_current_profile(self) -> Optional[str]:
        """
        Get current profile name
        
        Returns:
            str: Profile name or None
        """
        return self.current_profile
    
    def get_profile_path(self, profile_name: Optional[str] = None) -> Path:
        """
        Get path to profile directory
        
        Args:
            profile_name: Profile name (uses current if None)
            
        Returns:
            Path: Profile directory path
        """
        if profile_name:
            return self.profiles_directory / profile_name
        elif self.current_profile_path:
            return self.current_profile_path
        else:
            return self.profiles_directory / "default"
    
    def get_config_path(self, profile_name: Optional[str] = None) -> Path:
        """
        Get path to profile config file
        
        Args:
            profile_name: Profile name (uses current if None)
            
        Returns:
            Path: Config file path
        """
        return self.get_profile_path(profile_name) / "config.json"
    
    def get_logs_path(self, profile_name: Optional[str] = None) -> Path:
        """
        Get path to profile logs directory
        
        Args:
            profile_name: Profile name (uses current if None)
            
        Returns:
            Path: Logs directory path
        """
        return self.get_profile_path(profile_name) / "logs"
    
    def load_config(self, profile_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Load configuration for a profile
        
        Args:
            profile_name: Profile name (uses current if None)
            
        Returns:
            dict: Configuration data
        """
        config_path = self.get_config_path(profile_name)
        return load_json(config_path, self.DEFAULT_CONFIG)
    
    def save_config(self, config: Dict[str, Any], profile_name: Optional[str] = None) -> bool:
        """
        Save configuration for a profile
        
        Args:
            config: Configuration data
            profile_name: Profile name (uses current if None)
            
        Returns:
            bool: True if successful
        """
        config_path = self.get_config_path(profile_name)
        return save_json(config_path, config)
    
    def delete_profile(self, profile_name: str) -> bool:
        """
        Delete a profile
        
        Args:
            profile_name: Name of the profile to delete
            
        Returns:
            bool: True if successful
        """
        if profile_name == "default":
            print("❌ Cannot delete default profile")
            return False
        
        profile_path = self.profiles_directory / profile_name
        
        if not profile_path.exists():
            print(f"❌ Profile '{profile_name}' not found")
            return False
        
        try:
            import shutil
            shutil.rmtree(profile_path)
            print(f"✅ Deleted profile: {profile_name}")
            
            # If this was the current profile, switch to default
            if self.current_profile == profile_name:
                self.load_profile("default")
            
            return True
        except Exception as e:
            print(f"❌ Error deleting profile: {e}")
            return False
    
    def get_profile_info(self, profile_name: str) -> Optional[Dict]:
        """
        Get information about a profile
        
        Args:
            profile_name: Name of the profile
            
        Returns:
            dict: Profile information or None
        """
        profile_path = self.profiles_directory / profile_name
        
        if not profile_path.exists():
            return None
        
        metadata_path = profile_path / "metadata.json"
        metadata = load_json(metadata_path, {})
        
        # Count log files
        logs_path = profile_path / "logs"
        log_count = len(list(logs_path.glob('*.txt'))) if logs_path.exists() else 0
        
        return {
            'name': profile_name,
            'path': str(profile_path),
            'created': metadata.get('created', 'Unknown'),
            'last_used': metadata.get('last_used', 'Unknown'),
            'description': metadata.get('description', ''),
            'log_files': log_count
        }
    
    def export_profile(self, profile_name: str, export_path: Path) -> bool:
        """
        Export profile to a backup file
        
        Args:
            profile_name: Name of the profile to export
            export_path: Path to export file
            
        Returns:
            bool: True if successful
        """
        profile_path = self.profiles_directory / profile_name
        
        if not profile_path.exists():
            print(f"❌ Profile '{profile_name}' not found")
            return False
        
        try:
            import shutil
            shutil.make_archive(str(export_path.with_suffix('')), 'zip', profile_path)
            print(f"✅ Exported profile to: {export_path}.zip")
            return True
        except Exception as e:
            print(f"❌ Error exporting profile: {e}")
            return False
    
    def import_profile(self, import_path: Path, profile_name: str) -> bool:
        """
        Import profile from a backup file
        
        Args:
            import_path: Path to import file
            profile_name: Name for the imported profile
            
        Returns:
            bool: True if successful
        """
        if not import_path.exists():
            print(f"❌ Import file not found: {import_path}")
            return False
        
        profile_path = self.profiles_directory / profile_name
        
        if profile_path.exists():
            print(f"❌ Profile '{profile_name}' already exists")
            return False
        
        try:
            import shutil
            shutil.unpack_archive(str(import_path), profile_path)
            print(f"✅ Imported profile: {profile_name}")
            return True
        except Exception as e:
            print(f"❌ Error importing profile: {e}")
            return False
