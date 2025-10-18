"""
Utility Module
Provides common utility functions used across all modules
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional


def format_file_size(size_bytes: int) -> str:
    """
    Convert bytes to human-readable format
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        str: Formatted size (e.g., "1.5 MB", "500 KB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def get_file_size(file_path: Path) -> int:
    """
    Get file size in bytes
    
    Args:
        file_path: Path to the file
        
    Returns:
        int: File size in bytes, 0 if file doesn't exist
    """
    try:
        return file_path.stat().st_size if file_path.exists() else 0
    except Exception:
        return 0


def ensure_directory(directory: Path) -> None:
    """
    Ensure directory exists, create if it doesn't
    
    Args:
        directory: Path to directory
    """
    directory.mkdir(parents=True, exist_ok=True)


def load_json(file_path: Path, default: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Load JSON file with error handling
    
    Args:
        file_path: Path to JSON file
        default: Default value if file doesn't exist or is invalid
        
    Returns:
        dict: Loaded JSON data or default
    """
    if default is None:
        default = {}
    
    try:
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"⚠️ Error loading {file_path}: {e}")
    
    return default


def save_json(file_path: Path, data: Dict[str, Any], indent: int = 4) -> bool:
    """
    Save data to JSON file with error handling
    
    Args:
        file_path: Path to JSON file
        data: Data to save
        indent: JSON indentation level
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        ensure_directory(file_path.parent)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent)
        return True
    except IOError as e:
        print(f"❌ Error saving {file_path}: {e}")
        return False


def get_timestamp(format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Get current timestamp as formatted string
    
    Args:
        format_str: strftime format string
        
    Returns:
        str: Formatted timestamp
    """
    return datetime.now().strftime(format_str)


def get_date_string(format_str: str = "%Y-%m-%d") -> str:
    """
    Get current date as formatted string
    
    Args:
        format_str: strftime format string
        
    Returns:
        str: Formatted date
    """
    return datetime.now().strftime(format_str)


def is_junk_file(filename: str) -> bool:
    """
    Check if file is considered junk/temporary
    
    Args:
        filename: Name of the file
        
    Returns:
        bool: True if file is junk
    """
    junk_patterns = [
        '.tmp', '.temp', '.log', '.cache',
        'thumbs.db', 'desktop.ini', '.ds_store',
        '~$'  # Office temp files
    ]
    
    filename_lower = filename.lower()
    
    # Check if filename matches any junk pattern
    for pattern in junk_patterns:
        if filename_lower.endswith(pattern) or filename_lower.startswith(pattern):
            return True
    
    return False


def calculate_duration(start_time: datetime, end_time: Optional[datetime] = None) -> str:
    """
    Calculate duration between two times
    
    Args:
        start_time: Start datetime
        end_time: End datetime (defaults to now)
        
    Returns:
        str: Formatted duration (e.g., "2.5 seconds", "1 minute 30 seconds")
    """
    if end_time is None:
        end_time = datetime.now()
    
    duration = (end_time - start_time).total_seconds()
    
    if duration < 60:
        return f"{duration:.2f} seconds"
    elif duration < 3600:
        minutes = int(duration // 60)
        seconds = int(duration % 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''} {seconds} second{'s' if seconds != 1 else ''}"
    else:
        hours = int(duration // 3600)
        minutes = int((duration % 3600) // 60)
        return f"{hours} hour{'s' if hours != 1 else ''} {minutes} minute{'s' if minutes != 1 else ''}"


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing invalid characters
    
    Args:
        filename: Original filename
        
    Returns:
        str: Sanitized filename
    """
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename


def get_relative_path(file_path: Path, base_path: Path) -> str:
    """
    Get relative path from base path
    
    Args:
        file_path: Full file path
        base_path: Base directory path
        
    Returns:
        str: Relative path
    """
    try:
        return str(file_path.relative_to(base_path))
    except ValueError:
        return str(file_path)


def count_files_in_directory(directory: Path, recursive: bool = False) -> int:
    """
    Count files in a directory
    
    Args:
        directory: Directory path
        recursive: Whether to count recursively
        
    Returns:
        int: Number of files
    """
    if not directory.exists() or not directory.is_dir():
        return 0
    
    try:
        if recursive:
            return sum(1 for _ in directory.rglob('*') if _.is_file())
        else:
            return sum(1 for _ in directory.iterdir() if _.is_file())
    except Exception:
        return 0


def get_directory_size(directory: Path) -> int:
    """
    Calculate total size of directory
    
    Args:
        directory: Directory path
        
    Returns:
        int: Total size in bytes
    """
    if not directory.exists() or not directory.is_dir():
        return 0
    
    total_size = 0
    try:
        for file_path in directory.rglob('*'):
            if file_path.is_file():
                total_size += get_file_size(file_path)
    except Exception:
        pass
    
    return total_size
