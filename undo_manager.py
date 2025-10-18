"""
Undo Manager Module
Handles saving and restoring file move operations
"""

import json
import os
import shutil
from pathlib import Path
from datetime import datetime


class UndoManager:
    """Manages undo operations for file organization"""
    
    def __init__(self, log_file="undo_log.json"):
        """
        Initialize the undo manager
        
        Args:
            log_file: Path to the JSON file storing undo history
        """
        self.log_file = log_file
        self.current_session = []
    
    def add_move(self, original_path, new_path):
        """
        Record a file move operation
        
        Args:
            original_path: Original file location
            new_path: New file location after move
        """
        self.current_session.append({
            "original": str(original_path),
            "new": str(new_path)
        })
    
    def save_session(self):
        """Save the current session to the undo log file"""
        if not self.current_session:
            return False
        
        # Load existing log or create new one
        log_data = self._load_log()
        
        # Add new session with timestamp
        session_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "moves": self.current_session,
            "count": len(self.current_session)
        }
        
        log_data.append(session_entry)
        
        # Save to file
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=4)
        
        # Clear current session
        self.current_session = []
        return True
    
    def undo_last_session(self):
        """
        Undo the last organization session
        
        Returns:
            tuple: (success: bool, message: str, count: int)
        """
        log_data = self._load_log()
        
        if not log_data:
            return False, "No undo history found", 0
        
        # Get the last session
        last_session = log_data.pop()
        moves = last_session.get("moves", [])
        
        if not moves:
            return False, "No moves to undo", 0
        
        # Restore files to original locations
        restored_count = 0
        failed_files = []
        
        for move in moves:
            original_path = move["original"]
            new_path = move["new"]
            
            try:
                # Check if the file still exists at the new location
                if os.path.exists(new_path):
                    # Ensure original directory exists
                    os.makedirs(os.path.dirname(original_path), exist_ok=True)
                    
                    # Move file back
                    shutil.move(new_path, original_path)
                    restored_count += 1
                else:
                    failed_files.append(os.path.basename(new_path))
            except Exception as e:
                failed_files.append(f"{os.path.basename(new_path)} (Error: {str(e)})")
        
        # Update the log file (remove the undone session)
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=4)
        
        # Clean up empty category folders
        self._cleanup_empty_folders(moves)
        
        # Build result message
        if failed_files:
            message = f"Restored {restored_count} files. Failed: {', '.join(failed_files[:3])}"
            if len(failed_files) > 3:
                message += f" and {len(failed_files) - 3} more"
        else:
            message = f"Successfully restored {restored_count} files"
        
        return True, message, restored_count
    
    def _load_log(self):
        """Load the undo log from file"""
        if not os.path.exists(self.log_file):
            return []
        
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    
    def _cleanup_empty_folders(self, moves):
        """Remove empty category folders after undo"""
        folders_to_check = set()
        
        # Collect all folders that might be empty
        for move in moves:
            folder = os.path.dirname(move["new"])
            folders_to_check.add(folder)
        
        # Remove empty folders
        for folder in folders_to_check:
            try:
                if os.path.exists(folder) and not os.listdir(folder):
                    os.rmdir(folder)
            except OSError:
                pass  # Folder not empty or can't be removed
    
    def get_last_session_info(self):
        """
        Get information about the last session
        
        Returns:
            dict or None: Last session info or None if no history
        """
        log_data = self._load_log()
        return log_data[-1] if log_data else None
    
    def clear_session(self):
        """Clear the current session without saving"""
        self.current_session = []
