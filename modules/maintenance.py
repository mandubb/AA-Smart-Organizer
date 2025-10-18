"""
Maintenance Module
Handles system cleanup, junk file removal, and quick clean operations
"""

import os
import shutil
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from .utils import (
    is_junk_file, get_file_size, format_file_size,
    ensure_directory, get_timestamp
)


class MaintenanceManager:
    """Manages system maintenance and cleanup operations"""
    
    # Junk file patterns
    JUNK_EXTENSIONS = [
        '.tmp', '.temp', '.log', '.cache', '.bak',
        '.old', '.~', '.crdownload', '.part'
    ]
    
    JUNK_FILENAMES = [
        'thumbs.db', 'desktop.ini', '.ds_store',
        'icon\r', 'ehthumbs.db', 'ehthumbs_vista.db'
    ]
    
    # Office temporary files pattern
    OFFICE_TEMP_PREFIX = '~$'
    
    def __init__(self, log_callback=None):
        """
        Initialize maintenance manager
        
        Args:
            log_callback: Optional callback for logging messages
        """
        self.log_callback = log_callback
        self.cleaned_files: List[Dict] = []
        self.cleaned_folders: List[str] = []
        self.total_freed_space = 0
    
    def _log(self, message: str) -> None:
        """Send log message to callback or print"""
        if self.log_callback:
            self.log_callback(message)
        else:
            print(message)
    
    def is_junk_file(self, file_path: Path) -> Tuple[bool, str]:
        """
        Check if file is junk/temporary
        
        Args:
            file_path: Path to file
            
        Returns:
            Tuple of (is_junk: bool, reason: str)
        """
        filename = file_path.name.lower()
        
        # Check filename patterns
        if filename in self.JUNK_FILENAMES:
            return True, f"System file: {filename}"
        
        # Check Office temp files
        if filename.startswith(self.OFFICE_TEMP_PREFIX):
            return True, "Office temporary file"
        
        # Check extensions
        for ext in self.JUNK_EXTENSIONS:
            if filename.endswith(ext):
                return True, f"Temporary file ({ext})"
        
        return False, ""
    
    def scan_junk_files(self, directory: Path, recursive: bool = False) -> List[Dict]:
        """
        Scan directory for junk files
        
        Args:
            directory: Directory to scan
            recursive: Whether to scan subdirectories
            
        Returns:
            List of junk file information
        """
        junk_files = []
        
        if not directory.exists() or not directory.is_dir():
            self._log(f"⚠️ Invalid directory: {directory}")
            return junk_files
        
        try:
            # Get files to scan
            if recursive:
                files = [f for f in directory.rglob('*') if f.is_file()]
            else:
                files = [f for f in directory.iterdir() if f.is_file()]
            
            # Check each file
            for file_path in files:
                is_junk, reason = self.is_junk_file(file_path)
                if is_junk:
                    file_size = get_file_size(file_path)
                    junk_files.append({
                        'path': file_path,
                        'name': file_path.name,
                        'size': file_size,
                        'size_formatted': format_file_size(file_size),
                        'reason': reason
                    })
        
        except Exception as e:
            self._log(f"❌ Error scanning directory: {e}")
        
        return junk_files
    
    def find_empty_folders(self, directory: Path) -> List[Path]:
        """
        Find all empty folders in directory
        
        Args:
            directory: Directory to scan
            
        Returns:
            List of empty folder paths
        """
        empty_folders = []
        
        if not directory.exists() or not directory.is_dir():
            return empty_folders
        
        try:
            for folder in directory.rglob('*'):
                if folder.is_dir():
                    # Check if folder is empty (no files or subdirectories)
                    if not any(folder.iterdir()):
                        empty_folders.append(folder)
        except Exception as e:
            self._log(f"❌ Error finding empty folders: {e}")
        
        return empty_folders
    
    def delete_junk_files(self, junk_files: List[Dict]) -> Tuple[int, int]:
        """
        Delete junk files
        
        Args:
            junk_files: List of junk file information
            
        Returns:
            Tuple of (deleted_count, total_size_freed)
        """
        deleted_count = 0
        total_size = 0
        
        for file_info in junk_files:
            try:
                file_path = file_info['path']
                if file_path.exists():
                    file_size = file_info['size']
                    file_path.unlink()
                    deleted_count += 1
                    total_size += file_size
                    
                    self.cleaned_files.append({
                        'name': file_info['name'],
                        'path': str(file_path),
                        'size': file_size,
                        'reason': file_info['reason'],
                        'timestamp': get_timestamp()
                    })
            except Exception as e:
                self._log(f"⚠️ Could not delete {file_info['name']}: {e}")
        
        self.total_freed_space += total_size
        return deleted_count, total_size
    
    def delete_empty_folders(self, folders: List[Path]) -> int:
        """
        Delete empty folders
        
        Args:
            folders: List of folder paths
            
        Returns:
            int: Number of folders deleted
        """
        deleted_count = 0
        
        # Sort by depth (deepest first) to avoid issues with nested folders
        folders_sorted = sorted(folders, key=lambda p: len(p.parts), reverse=True)
        
        for folder in folders_sorted:
            try:
                if folder.exists() and folder.is_dir():
                    # Double-check it's still empty
                    if not any(folder.iterdir()):
                        folder.rmdir()
                        deleted_count += 1
                        self.cleaned_folders.append(str(folder))
            except Exception as e:
                self._log(f"⚠️ Could not delete folder {folder}: {e}")
        
        return deleted_count
    
    def clear_recycle_bin_windows(self) -> bool:
        """
        Clear Windows Recycle Bin (Windows only)
        
        Returns:
            bool: True if successful
        """
        try:
            import ctypes
            from ctypes import wintypes
            
            # SHEmptyRecycleBin flags
            SHERB_NOCONFIRMATION = 0x00000001
            SHERB_NOPROGRESSUI = 0x00000002
            SHERB_NOSOUND = 0x00000004
            
            result = ctypes.windll.shell32.SHEmptyRecycleBinW(
                None,
                None,
                SHERB_NOCONFIRMATION | SHERB_NOPROGRESSUI | SHERB_NOSOUND
            )
            
            return result == 0
        except Exception as e:
            self._log(f"⚠️ Could not clear Recycle Bin: {e}")
            return False
    
    def quick_clean(
        self,
        directory: Path,
        recursive: bool = False,
        preview_only: bool = False,
        clear_recycle_bin: bool = False
    ) -> Dict:
        """
        Perform quick clean operation
        
        Args:
            directory: Directory to clean
            recursive: Whether to clean subdirectories
            preview_only: If True, only scan without deleting
            clear_recycle_bin: Whether to clear Recycle Bin (Windows)
            
        Returns:
            dict: Cleanup statistics
        """
        self._log("\n" + "="*60)
        self._log("🧹 Quick Clean Mode")
        self._log("="*60)
        
        # Reset counters
        self.cleaned_files = []
        self.cleaned_folders = []
        self.total_freed_space = 0
        
        # Scan for junk files
        self._log(f"\n🔍 Scanning for junk files in: {directory}")
        junk_files = self.scan_junk_files(directory, recursive)
        
        if not junk_files:
            self._log("✅ No junk files found!")
        else:
            self._log(f"\n📋 Found {len(junk_files)} junk files:")
            total_size = sum(f['size'] for f in junk_files)
            self._log(f"   Total size: {format_file_size(total_size)}")
            
            # Show preview
            for file_info in junk_files[:10]:  # Show first 10
                self._log(f"   • {file_info['name']} ({file_info['size_formatted']}) - {file_info['reason']}")
            
            if len(junk_files) > 10:
                self._log(f"   ... and {len(junk_files) - 10} more")
            
            if not preview_only:
                self._log("\n🗑️ Deleting junk files...")
                deleted, freed = self.delete_junk_files(junk_files)
                self._log(f"✅ Deleted {deleted} files, freed {format_file_size(freed)}")
        
        # Find empty folders
        self._log("\n🔍 Scanning for empty folders...")
        empty_folders = self.find_empty_folders(directory)
        
        if not empty_folders:
            self._log("✅ No empty folders found!")
        else:
            self._log(f"\n📋 Found {len(empty_folders)} empty folders")
            
            if not preview_only:
                self._log("\n🗑️ Deleting empty folders...")
                deleted_folders = self.delete_empty_folders(empty_folders)
                self._log(f"✅ Deleted {deleted_folders} empty folders")
        
        # Clear Recycle Bin (Windows only)
        recycle_bin_cleared = False
        if clear_recycle_bin and not preview_only:
            if os.name == 'nt':  # Windows
                self._log("\n🗑️ Clearing Recycle Bin...")
                if self.clear_recycle_bin_windows():
                    self._log("✅ Recycle Bin cleared")
                    recycle_bin_cleared = True
                else:
                    self._log("⚠️ Could not clear Recycle Bin")
            else:
                self._log("⚠️ Recycle Bin clearing only supported on Windows")
        
        # Summary
        stats = {
            'junk_files_found': len(junk_files),
            'junk_files_deleted': len(self.cleaned_files),
            'empty_folders_found': len(empty_folders),
            'empty_folders_deleted': len(self.cleaned_folders),
            'space_freed': self.total_freed_space,
            'space_freed_formatted': format_file_size(self.total_freed_space),
            'recycle_bin_cleared': recycle_bin_cleared,
            'preview_only': preview_only
        }
        
        self._log("\n" + "="*60)
        self._log("📊 Quick Clean Summary")
        self._log("="*60)
        self._log(f"Junk files: {stats['junk_files_deleted']}/{stats['junk_files_found']}")
        self._log(f"Empty folders: {stats['empty_folders_deleted']}/{stats['empty_folders_found']}")
        self._log(f"Space freed: {stats['space_freed_formatted']}")
        if recycle_bin_cleared:
            self._log("Recycle Bin: Cleared")
        self._log("="*60 + "\n")
        
        return stats
    
    def get_cleanup_report(self) -> str:
        """
        Get detailed cleanup report
        
        Returns:
            str: Formatted report
        """
        report = []
        report.append("="*60)
        report.append("CLEANUP REPORT")
        report.append("="*60)
        report.append(f"Generated: {get_timestamp()}")
        report.append("")
        
        report.append(f"Files Cleaned: {len(self.cleaned_files)}")
        report.append(f"Folders Cleaned: {len(self.cleaned_folders)}")
        report.append(f"Total Space Freed: {format_file_size(self.total_freed_space)}")
        report.append("")
        
        if self.cleaned_files:
            report.append("CLEANED FILES:")
            for file_info in self.cleaned_files:
                report.append(f"  • {file_info['name']} - {format_file_size(file_info['size'])} - {file_info['reason']}")
            report.append("")
        
        if self.cleaned_folders:
            report.append("CLEANED FOLDERS:")
            for folder in self.cleaned_folders:
                report.append(f"  • {folder}")
            report.append("")
        
        report.append("="*60)
        
        return "\n".join(report)
