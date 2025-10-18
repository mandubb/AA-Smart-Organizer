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
    
    def __init__(self, config_file="config.json"):
        """
        Initialize the file organizer
        
        Args:
            config_file: Path to the configuration file containing categories
        """
        self.config_file = config_file
        self.categories = self._load_categories()
        self.stats = defaultdict(int)
    
    def _load_categories(self):
        """Load file categories from config file"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config.get("categories", {})
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading config: {e}")
            # Return default categories if config fails
            return {
                "Documents": [".pdf", ".docx", ".txt"],
                "Images": [".jpg", ".jpeg", ".png"],
                "Videos": [".mp4", ".mkv"],
                "Music": [".mp3", ".wav"],
                "Installers": [".exe", ".msi"]
            }
    
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
