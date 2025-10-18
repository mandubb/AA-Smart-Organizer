"""
Activity Log Module
Tracks all file operations with detailed logging and undo support
"""

import csv
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from .utils import (
    ensure_directory, get_timestamp, get_date_string,
    format_file_size, get_file_size, save_json, load_json
)


class ActivityLog:
    """Manages activity logging for file operations"""
    
    def __init__(self, log_directory: Path):
        """
        Initialize activity log
        
        Args:
            log_directory: Directory to store log files
        """
        self.log_directory = Path(log_directory)
        ensure_directory(self.log_directory)
        
        self.current_session: List[Dict] = []
        self.log_file = self.log_directory / f"activity_{get_date_string()}.txt"
        self.csv_file = self.log_directory / f"activity_{get_date_string()}.csv"
        self.undo_file = self.log_directory / "undo_data.json"
        
        # Initialize CSV file with headers if it doesn't exist
        if not self.csv_file.exists():
            self._initialize_csv()
    
    def _initialize_csv(self) -> None:
        """Initialize CSV file with headers"""
        try:
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'Timestamp', 'Action', 'Filename', 'Old Path', 
                    'New Path', 'File Size', 'Category', 'Status'
                ])
        except IOError as e:
            print(f"⚠️ Could not initialize CSV: {e}")
    
    def log_move(
        self,
        filename: str,
        old_path: Path,
        new_path: Path,
        file_size: int,
        category: str,
        status: str = "Success"
    ) -> None:
        """
        Log a file move operation
        
        Args:
            filename: Name of the file
            old_path: Original file path
            new_path: New file path
            file_size: Size of file in bytes
            category: Category the file was moved to
            status: Operation status (Success/Failed)
        """
        timestamp = get_timestamp()
        
        # Create log entry
        entry = {
            'timestamp': timestamp,
            'action': 'MOVE',
            'filename': filename,
            'old_path': str(old_path),
            'new_path': str(new_path),
            'file_size': file_size,
            'file_size_formatted': format_file_size(file_size),
            'category': category,
            'status': status
        }
        
        # Add to current session
        self.current_session.append(entry)
        
        # Write to text log
        self._write_to_text_log(entry)
        
        # Write to CSV log
        self._write_to_csv_log(entry)
    
    def log_delete(
        self,
        filename: str,
        file_path: Path,
        file_size: int,
        reason: str = "Junk file",
        status: str = "Success"
    ) -> None:
        """
        Log a file deletion operation
        
        Args:
            filename: Name of the file
            file_path: Path to deleted file
            file_size: Size of file in bytes
            reason: Reason for deletion
            status: Operation status
        """
        timestamp = get_timestamp()
        
        entry = {
            'timestamp': timestamp,
            'action': 'DELETE',
            'filename': filename,
            'old_path': str(file_path),
            'new_path': 'DELETED',
            'file_size': file_size,
            'file_size_formatted': format_file_size(file_size),
            'category': reason,
            'status': status
        }
        
        self.current_session.append(entry)
        self._write_to_text_log(entry)
        self._write_to_csv_log(entry)
    
    def log_action(
        self,
        action: str,
        description: str,
        details: Optional[Dict] = None
    ) -> None:
        """
        Log a general action
        
        Args:
            action: Action type
            description: Action description
            details: Additional details
        """
        timestamp = get_timestamp()
        
        entry = {
            'timestamp': timestamp,
            'action': action,
            'description': description,
            'details': details or {}
        }
        
        # Write to text log only
        log_line = f"[{timestamp}] {action}: {description}"
        if details:
            log_line += f" | Details: {details}"
        
        self._append_to_text_log(log_line)
    
    def _write_to_text_log(self, entry: Dict) -> None:
        """Write entry to text log file"""
        try:
            log_line = (
                f"[{entry['timestamp']}] {entry['action']}: "
                f"{entry['filename']} | "
                f"From: {entry['old_path']} → To: {entry['new_path']} | "
                f"Size: {entry['file_size_formatted']} | "
                f"Category: {entry['category']} | "
                f"Status: {entry['status']}"
            )
            self._append_to_text_log(log_line)
        except Exception as e:
            print(f"⚠️ Error writing to text log: {e}")
    
    def _append_to_text_log(self, line: str) -> None:
        """Append a line to text log file"""
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(line + '\n')
        except IOError as e:
            print(f"⚠️ Error appending to log: {e}")
    
    def _write_to_csv_log(self, entry: Dict) -> None:
        """Write entry to CSV log file"""
        try:
            with open(self.csv_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    entry['timestamp'],
                    entry['action'],
                    entry['filename'],
                    entry['old_path'],
                    entry['new_path'],
                    entry['file_size_formatted'],
                    entry['category'],
                    entry['status']
                ])
        except IOError as e:
            print(f"⚠️ Error writing to CSV: {e}")
    
    def save_undo_data(self) -> bool:
        """
        Save current session for undo capability
        
        Returns:
            bool: True if successful
        """
        if not self.current_session:
            return False
        
        # Filter only successful move operations
        undo_data = [
            entry for entry in self.current_session
            if entry['action'] == 'MOVE' and entry['status'] == 'Success'
        ]
        
        if not undo_data:
            return False
        
        # Save to undo file
        return save_json(self.undo_file, {
            'timestamp': get_timestamp(),
            'operations': undo_data
        })
    
    def load_undo_data(self) -> Optional[List[Dict]]:
        """
        Load undo data from last session
        
        Returns:
            List of operations or None
        """
        data = load_json(self.undo_file)
        return data.get('operations') if data else None
    
    def clear_undo_data(self) -> None:
        """Clear undo data file"""
        if self.undo_file.exists():
            self.undo_file.unlink()
    
    def get_session_summary(self) -> Dict:
        """
        Get summary of current session
        
        Returns:
            dict: Session statistics
        """
        if not self.current_session:
            return {
                'total_operations': 0,
                'moves': 0,
                'deletes': 0,
                'total_size': 0,
                'categories': {}
            }
        
        moves = sum(1 for e in self.current_session if e['action'] == 'MOVE')
        deletes = sum(1 for e in self.current_session if e['action'] == 'DELETE')
        total_size = sum(e.get('file_size', 0) for e in self.current_session)
        
        # Count by category
        categories = {}
        for entry in self.current_session:
            if entry['action'] == 'MOVE':
                cat = entry.get('category', 'Unknown')
                categories[cat] = categories.get(cat, 0) + 1
        
        return {
            'total_operations': len(self.current_session),
            'moves': moves,
            'deletes': deletes,
            'total_size': total_size,
            'total_size_formatted': format_file_size(total_size),
            'categories': categories
        }
    
    def clear_session(self) -> None:
        """Clear current session data"""
        self.current_session = []
    
    def rotate_logs(self, keep_days: int = 30) -> int:
        """
        Rotate old log files (delete logs older than keep_days)
        
        Args:
            keep_days: Number of days to keep logs
            
        Returns:
            int: Number of files deleted
        """
        deleted_count = 0
        cutoff_date = datetime.now().timestamp() - (keep_days * 86400)
        
        try:
            for log_file in self.log_directory.glob('activity_*.txt'):
                if log_file.stat().st_mtime < cutoff_date:
                    log_file.unlink()
                    deleted_count += 1
            
            for csv_file in self.log_directory.glob('activity_*.csv'):
                if csv_file.stat().st_mtime < cutoff_date:
                    csv_file.unlink()
                    deleted_count += 1
        except Exception as e:
            print(f"⚠️ Error rotating logs: {e}")
        
        return deleted_count
    
    def export_session_to_file(self, output_path: Path) -> bool:
        """
        Export current session to a text file
        
        Args:
            output_path: Path to output file
            
        Returns:
            bool: True if successful
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("="*70 + "\n")
                f.write("AA Smart Organizer - Session Report\n")
                f.write(f"Generated: {get_timestamp()}\n")
                f.write("="*70 + "\n\n")
                
                summary = self.get_session_summary()
                f.write("SUMMARY:\n")
                f.write(f"  Total Operations: {summary['total_operations']}\n")
                f.write(f"  Files Moved: {summary['moves']}\n")
                f.write(f"  Files Deleted: {summary['deletes']}\n")
                f.write(f"  Total Size: {summary['total_size_formatted']}\n\n")
                
                if summary['categories']:
                    f.write("BY CATEGORY:\n")
                    for cat, count in summary['categories'].items():
                        f.write(f"  {cat}: {count} files\n")
                    f.write("\n")
                
                f.write("DETAILED LOG:\n")
                f.write("-"*70 + "\n")
                for entry in self.current_session:
                    f.write(f"[{entry['timestamp']}] {entry['action']}: {entry['filename']}\n")
                    f.write(f"  From: {entry['old_path']}\n")
                    f.write(f"  To: {entry['new_path']}\n")
                    f.write(f"  Size: {entry.get('file_size_formatted', 'N/A')}\n")
                    f.write(f"  Category: {entry.get('category', 'N/A')}\n")
                    f.write(f"  Status: {entry['status']}\n")
                    f.write("-"*70 + "\n")
            
            return True
        except IOError as e:
            print(f"❌ Error exporting session: {e}")
            return False
