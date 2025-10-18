"""
AA Smart Organizer - CLI Interface
Command-line interface for the modular file organization system
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime

# Import modules
from modules import (
    ProfileManager, ActivityLog, MaintenanceManager,
    SummaryGenerator, TaskScheduler, format_file_size
)
from organizer import FileOrganizer


class AASmartOrganizerCLI:
    """CLI interface for AA Smart Organizer"""
    
    def __init__(self):
        """Initialize CLI application"""
        self.base_path = Path(__file__).parent
        self.profiles_path = self.base_path / "profiles"
        self.logs_path = self.base_path / "logs"
        
        # Initialize profile manager
        self.profile_manager = ProfileManager(self.profiles_path)
        self.profile_manager.load_profile("default")
        
        # Load configuration
        self.config = self.profile_manager.load_config()
        
        # Initialize components
        self.activity_log = None
        self.maintenance = None
        self.summary = None
        self.organizer = None
        
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize all components based on configuration"""
        # Activity Log
        if self.config.get('enable_activity_log', True):
            log_path = self.profile_manager.get_logs_path()
            self.activity_log = ActivityLog(log_path)
        
        # Maintenance Manager
        if self.config.get('enable_quick_clean', True):
            self.maintenance = MaintenanceManager(log_callback=self._log)
        
        # Summary Generator
        if self.config.get('enable_summary', True):
            self.summary = SummaryGenerator()
        
        # File Organizer
        config_path = self.profile_manager.get_config_path()
        self.organizer = FileOrganizer(
            config_file=str(config_path),
            log_callback=self._log
        )
    
    def _log(self, message: str):
        """Log message to console"""
        print(message)
    
    def organize(self, folder_path: str, quick_clean: bool = False):
        """
        Organize files in a folder
        
        Args:
            folder_path: Path to folder to organize
            quick_clean: Whether to run quick clean first
        """
        folder = Path(folder_path)
        
        if not folder.exists() or not folder.is_dir():
            print(f"❌ Invalid folder path: {folder_path}")
            return
        
        print("\n" + "="*70)
        print(f"🗂️  AA SMART ORGANIZER - {self.profile_manager.get_current_profile().upper()} PROFILE")
        print("="*70)
        print(f"Target Folder: {folder}")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70 + "\n")
        
        # Quick Clean first if requested
        if quick_clean and self.maintenance:
            print("🧹 Running Quick Clean first...")
            self.maintenance.quick_clean(
                folder,
                recursive=False,
                preview_only=False,
                clear_recycle_bin=self.config.get('maintenance', {}).get('clear_recycle_bin', False)
            )
            print()
        
        # Start summary tracking
        if self.summary:
            self.summary.start_operation()
        
        # Clear activity log session
        if self.activity_log:
            self.activity_log.clear_session()
        
        # Get file count
        total_files, organizable = self.organizer.get_organizable_count(folder)
        print(f"📊 Found {total_files} files, {organizable} can be organized\n")
        
        if organizable == 0:
            print("✅ No files to organize!")
            return
        
        # Organize files
        print("🚀 Organizing files...\n")
        
        try:
            stats = {}
            files_organized = 0
            total_size = 0
            
            # Get all files
            files = [f for f in folder.iterdir() if f.is_file()]
            
            for index, file_path in enumerate(files, 1):
                try:
                    file_extension = file_path.suffix
                    if not file_extension:
                        continue
                    
                    category = self.organizer.get_category(file_extension)
                    if not category:
                        continue
                    
                    # Create category folder
                    category_folder = folder / category
                    category_folder.mkdir(exist_ok=True)
                    
                    # Build new path
                    new_path = category_folder / file_path.name
                    
                    # Handle duplicates
                    if new_path.exists():
                        new_path = self.organizer._get_unique_filename(new_path)
                    
                    # Get file size
                    file_size = file_path.stat().st_size
                    
                    # Move file
                    import shutil
                    shutil.move(str(file_path), str(new_path))
                    
                    # Log the move
                    if self.activity_log:
                        self.activity_log.log_move(
                            file_path.name,
                            file_path,
                            new_path,
                            file_size,
                            category,
                            "Success"
                        )
                    
                    # Update stats
                    stats[category] = stats.get(category, 0) + 1
                    files_organized += 1
                    total_size += file_size
                    
                    # Progress indicator
                    if index % 10 == 0 or index == len(files):
                        print(f"  Progress: {index}/{len(files)} files processed...", end='\r')
                
                except Exception as e:
                    print(f"\n⚠️  Error moving {file_path.name}: {e}")
                    continue
            
            print("\n")
            
            # Save undo data
            if self.activity_log:
                self.activity_log.save_undo_data()
            
            # Generate summary
            if self.summary:
                self.summary.end_operation()
                summary_data = self.summary.generate_summary(
                    total_files=total_files,
                    files_organized=files_organized,
                    files_skipped=total_files - organizable,
                    files_failed=organizable - files_organized,
                    total_size=total_size,
                    categories=stats
                )
                
                # Print summary
                self.summary.print_cli_summary(summary_data)
                
                # Export summary
                summary_file = self.logs_path / f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                self.summary.export_to_text(summary_file)
                print(f"📄 Summary saved to: {summary_file}\n")
            
            # Rotate logs if needed
            if self.activity_log:
                rotation_days = self.config.get('log_rotation_days', 30)
                deleted = self.activity_log.rotate_logs(rotation_days)
                if deleted > 0:
                    print(f"🗑️  Rotated {deleted} old log files\n")
        
        except Exception as e:
            print(f"\n❌ Error during organization: {e}")
            import traceback
            traceback.print_exc()
    
    def quick_clean(self, folder_path: str, preview: bool = False):
        """
        Run quick clean on a folder
        
        Args:
            folder_path: Path to folder to clean
            preview: If True, only preview without deleting
        """
        if not self.maintenance:
            print("❌ Quick Clean is disabled in configuration")
            return
        
        folder = Path(folder_path)
        
        if not folder.exists() or not folder.is_dir():
            print(f"❌ Invalid folder path: {folder_path}")
            return
        
        self.maintenance.quick_clean(
            folder,
            recursive=False,
            preview_only=preview,
            clear_recycle_bin=self.config.get('maintenance', {}).get('clear_recycle_bin', False)
        )
    
    def list_profiles(self):
        """List all available profiles"""
        profiles = self.profile_manager.list_profiles()
        current = self.profile_manager.get_current_profile()
        
        print("\n" + "="*70)
        print("📋 AVAILABLE PROFILES")
        print("="*70)
        
        for profile in profiles:
            info = self.profile_manager.get_profile_info(profile)
            marker = "→" if profile == current else " "
            print(f"{marker} {profile}")
            if info:
                print(f"    Created: {info['created']}")
                print(f"    Last Used: {info['last_used']}")
                print(f"    Log Files: {info['log_files']}")
        
        print("="*70 + "\n")
    
    def switch_profile(self, profile_name: str):
        """Switch to a different profile"""
        if self.profile_manager.load_profile(profile_name):
            self.config = self.profile_manager.load_config()
            self._initialize_components()
            print(f"✅ Switched to profile: {profile_name}")
        else:
            print(f"❌ Failed to switch to profile: {profile_name}")
    
    def create_profile(self, profile_name: str):
        """Create a new profile"""
        if self.profile_manager.create_profile(profile_name):
            print(f"✅ Created profile: {profile_name}")
        else:
            print(f"❌ Failed to create profile: {profile_name}")


def main():
    """Main entry point for CLI"""
    parser = argparse.ArgumentParser(
        description="AA Smart Organizer - Professional File Organization Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main_cli.py organize "C:\\Downloads"
  python main_cli.py organize "C:\\Downloads" --quick-clean
  python main_cli.py quick-clean "C:\\Downloads" --preview
  python main_cli.py list-profiles
  python main_cli.py switch-profile work
  python main_cli.py create-profile client1

Made with ❤️ by AA's Computer and Remote Services
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Organize command
    organize_parser = subparsers.add_parser('organize', help='Organize files in a folder')
    organize_parser.add_argument('folder', help='Path to folder to organize')
    organize_parser.add_argument('--quick-clean', action='store_true', help='Run quick clean first')
    
    # Quick clean command
    clean_parser = subparsers.add_parser('quick-clean', help='Run quick clean on a folder')
    clean_parser.add_argument('folder', help='Path to folder to clean')
    clean_parser.add_argument('--preview', action='store_true', help='Preview only, do not delete')
    
    # Profile commands
    subparsers.add_parser('list-profiles', help='List all profiles')
    
    switch_parser = subparsers.add_parser('switch-profile', help='Switch to a different profile')
    switch_parser.add_argument('profile', help='Profile name')
    
    create_parser = subparsers.add_parser('create-profile', help='Create a new profile')
    create_parser.add_argument('profile', help='Profile name')
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize CLI
    try:
        cli = AASmartOrganizerCLI()
        
        # Execute command
        if args.command == 'organize':
            cli.organize(args.folder, quick_clean=args.quick_clean)
        
        elif args.command == 'quick-clean':
            cli.quick_clean(args.folder, preview=args.preview)
        
        elif args.command == 'list-profiles':
            cli.list_profiles()
        
        elif args.command == 'switch-profile':
            cli.switch_profile(args.profile)
        
        elif args.command == 'create-profile':
            cli.create_profile(args.profile)
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Operation cancelled by user")
        sys.exit(0)
    
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
