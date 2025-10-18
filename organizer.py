"""
File Organizer Module
Handles the core logic for organizing files into categorized folders
"""

import os
import shutil
import json
from pathlib import Path
from collections import defaultdict


class FileOrganizer:
    """Organizes files into categorized subfolders"""
    
    # Default configuration structure
    DEFAULT_CONFIG = {
        "file_types": {
            "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".xls", ".pptx", ".ppt", ".odt", ".rtf", ".csv", ".md"],
            "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".ico", ".webp", ".tiff", ".heic", ".raw"],
            "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".m4v", ".3gp", ".mts"],
            "Music": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a", ".mid", ".midi"],
            "Installers": [".exe", ".msi", ".dmg", ".pkg", ".deb", ".rpm", ".apk", ".appimage"],
            "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".iso"],
            "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".h", ".json", ".xml", ".sql", ".php", ".ts", ".sh", ".bat", ".yml", ".yaml"],
            "Game Files": [".iso", ".bin", ".cue", ".sav", ".pak", ".vpk", ".wad", ".rom", ".nes", ".gba", ".n64", ".rpf"],
            "System": [".bat", ".cmd", ".reg", ".inf", ".sys", ".dll", ".ini", ".cfg", ".log", ".tmp"],
            "Design": [".psd", ".ai", ".xd", ".fig", ".blend", ".fbx", ".obj", ".3ds", ".prproj", ".aep", ".kra", ".xcf"],
            "Backups": [".img", ".vhd", ".vhdx", ".bak", ".gho", ".tar.gz"],
            "eBooks": [".epub", ".mobi", ".azw3", ".cbz", ".cbr", ".pdf"],
            "Plugins & Mods": [".dll", ".pak", ".vst", ".vst3", ".esp", ".bsa", ".mod", ".asi"],
            "Torrents": [".torrent"],
            "Miscellaneous": []
        }
    }
    
    def __init__(self, config_file="config.json", log_callback=None):
        """
        Initialize the file organizer
        
        Args:
            config_file: Path to the configuration file containing categories
            log_callback: Optional callback function for logging messages
        """
        self.config_file = config_file
        self.log_callback = log_callback
        self.categories = self._load_categories()
        self.stats = defaultdict(int)
    
    def _log(self, message):
        """Send log message to callback if available"""
        if self.log_callback:
            self.log_callback(message)
        else:
            print(message)
    
    def _load_categories(self):
        """
        Load file categories from config file with validation and auto-regeneration
        
        Returns:
            dict: File type categories
        """
        try:
            # Try to load existing config
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Validate structure - check for 'file_types' key
            if "file_types" not in config:
                # Check for old 'categories' key for backward compatibility
                if "categories" in config:
                    self._log("⚠️ Old config format detected, migrating to new format...")
                    config["file_types"] = config.pop("categories")
                    self._save_config(config)
                    self._log("✅ Config migrated successfully")
                else:
                    raise ValueError("Invalid config structure: missing 'file_types' key")
            
            # Validate that file_types is a dictionary
            if not isinstance(config["file_types"], dict):
                raise ValueError("Invalid config: 'file_types' must be a dictionary")
            
            # Validate each category has a list of extensions
            for category, extensions in config["file_types"].items():
                if not isinstance(extensions, list):
                    raise ValueError(f"Invalid config: '{category}' must have a list of extensions")
            
            self._log("✅ Loaded file type configuration from config.json")
            return config["file_types"]
            
        except FileNotFoundError:
            self._log("⚠️ config.json not found, creating default configuration...")
            self._regenerate_config()
            self._log("✅ Default config.json created successfully")
            return self.DEFAULT_CONFIG["file_types"]
            
        except (json.JSONDecodeError, ValueError) as e:
            self._log(f"⚠️ Config error: {e}")
            self._log("🔄 Regenerating config.json with default values...")
            self._regenerate_config()
            self._log("✅ Config regenerated successfully")
            return self.DEFAULT_CONFIG["file_types"]
    
    def _regenerate_config(self):
        """Regenerate config.json with default values"""
        self._save_config(self.DEFAULT_CONFIG)
    
    def _save_config(self, config):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4)
        except IOError as e:
            self._log(f"❌ Error saving config: {e}")
    
    def reload_config(self):
        """
        Reload configuration from file
        
        Returns:
            tuple: (success: bool, message: str, category_count: int)
        """
        try:
            old_count = len(self.categories)
            self.categories = self._load_categories()
            new_count = len(self.categories)
            
            if new_count != old_count:
                message = f"Config reloaded: {new_count} categories (was {old_count})"
            else:
                message = f"Config reloaded: {new_count} categories"
            
            return True, message, new_count
        except Exception as e:
            return False, f"Failed to reload config: {str(e)}", 0
    
    def get_category(self, file_extension):
        """
        Determine the category for a file based on its extension
        
        Args:
            file_extension: File extension (e.g., '.pdf')
        
        Returns:
            str or None: Category name or None if not categorized
        """
        file_extension = file_extension.lower()
        
        for category, extensions in self.categories.items():
            if file_extension in [ext.lower() for ext in extensions]:
                return category
        
        return None
    
    def organize_folder(self, folder_path, progress_callback=None, undo_manager=None):
        """
        Organize files in the specified folder
        
        Args:
            folder_path: Path to the folder to organize
            progress_callback: Optional callback function(current, total, filename)
            undo_manager: Optional UndoManager instance to track moves
        
        Returns:
            dict: Statistics about the organization (files moved per category)
        """
        folder_path = Path(folder_path)
        
        if not folder_path.exists() or not folder_path.is_dir():
            raise ValueError(f"Invalid folder path: {folder_path}")
        
        # Reset statistics
        self.stats = defaultdict(int)
        
        # Get all files in the folder (not in subdirectories)
        files = [f for f in folder_path.iterdir() if f.is_file()]
        total_files = len(files)
        
        if total_files == 0:
            return self.stats
        
        # Process each file
        for index, file_path in enumerate(files, 1):
            try:
                # Get file extension
                file_extension = file_path.suffix
                
                # Skip if no extension
                if not file_extension:
                    continue
                
                # Determine category
                category = self.get_category(file_extension)
                
                # Skip if file doesn't belong to any category
                if not category:
                    continue
                
                # Create category folder if it doesn't exist
                category_folder = folder_path / category
                category_folder.mkdir(exist_ok=True)
                
                # Build new file path
                new_path = category_folder / file_path.name
                
                # Handle duplicate filenames
                if new_path.exists():
                    new_path = self._get_unique_filename(new_path)
                
                # Move the file
                original_path = file_path
                shutil.move(str(file_path), str(new_path))
                
                # Track the move for undo
                if undo_manager:
                    undo_manager.add_move(original_path, new_path)
                
                # Update statistics
                self.stats[category] += 1
                
                # Call progress callback
                if progress_callback:
                    progress_callback(index, total_files, file_path.name)
                
            except Exception as e:
                print(f"Error moving {file_path.name}: {e}")
                continue
        
        return dict(self.stats)
    
    def _get_unique_filename(self, file_path):
        """
        Generate a unique filename if a file already exists
        
        Args:
            file_path: Path object for the file
        
        Returns:
            Path: Unique file path
        """
        file_path = Path(file_path)
        base_name = file_path.stem
        extension = file_path.suffix
        parent = file_path.parent
        counter = 1
        
        while True:
            new_name = f"{base_name}_{counter}{extension}"
            new_path = parent / new_name
            
            if not new_path.exists():
                return new_path
            
            counter += 1
    
    def get_organizable_count(self, folder_path):
        """
        Count how many files can be organized in the folder
        
        Args:
            folder_path: Path to the folder
        
        Returns:
            tuple: (total_files, organizable_files)
        """
        folder_path = Path(folder_path)
        
        if not folder_path.exists() or not folder_path.is_dir():
            return 0, 0
        
        files = [f for f in folder_path.iterdir() if f.is_file()]
        total_files = len(files)
        
        organizable_files = sum(
            1 for f in files 
            if f.suffix and self.get_category(f.suffix)
        )
        
        return total_files, organizable_files
    
    def get_categories_list(self):
        """Get list of all available categories"""
        return list(self.categories.keys())
